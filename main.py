from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from document_loader import load_file
from vector_store import embed_and_store, search_similar
from openai import OpenAI
import os
from dotenv import load_dotenv
from groq import Groq
from document_loader import load_image
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  



# Load environment variables
load_dotenv()


# client = OpenAI(
#     api_key=os.getenv("API_KEY")
# )

client = Groq(api_key=os.getenv("API_KEY"))

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)

# Initialize FastAPI
app = FastAPI()

# Pydantic model for query input
class QueryPayload(BaseModel):
    question: str

# Upload endpoint
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        # Check if filename exists
        if not file.filename:
            return {"error": "No filename provided"}

        # Process image files
        if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            text = load_image(file)
            embed_and_store(text, {"filename": file.filename})
            return {"status": "uploaded and indexed", "text": text}
            
        # Process other files
        contents = await file.read()
        path = f"temp/{file.filename}"
        with open(path, "wb") as f:
            f.write(contents)
        text = load_file(path)
        embed_and_store(text, {"filename": file.filename})
        return {"status": "uploaded and indexed"}
        
    except Exception as e:
        return {"error": str(e)}

# Query endpoint using DeepSeek
@app.post("/query")
async def query_api(payload: QueryPayload):
    question = payload.question
    try:
        results = search_similar(question)
        if not results:
            return {
                "answer": "No relevant documents found.",
                "context": "",
                "sources": []
            }

        context = "\n".join([chunk for chunk, _ in results])
        prompt = f"Answer using the context below:\n{context}\n\nQuestion: {question}"

        # response = client.chat.completions.create(
        #     model="meta-llama/llama-4-scout-17b-16e-instruct",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # or another model Groq supports
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False
        )

        answer = response.choices[0].message.content
        sources = [meta['filename'] for _, meta in results]

        return {
            "answer": answer,
            "context": context,
            "sources": sources
        }

    except Exception as e:
        return {"error": str(e)}
