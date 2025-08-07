# GenAI_ChatBot
# RAG Chatbot with FastAPI

This project is a Retrieval-Augmented Generation (RAG) API that extracts information from various document types and answers questions using LLMs.

---

## 🚀 Features

- Upload and parse `.pdf`, `.docx`, `.txt`, `.csv`, `.jpg`, `.png` files
- Extracts and chunks content
- Generates and stores embeddings using SentenceTransformers + FAISS
- Accepts text queries
- Returns answers with context and source file info
- Supports OCR for images
- Built with FastAPI

---

## 📦 Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd rag-chatbot
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt

```
### 2. Add Environment Variables

```bash

OPENAI_API_KEY=openai_key


```

###