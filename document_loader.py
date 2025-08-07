import pdfplumber, pytesseract, pandas as pd
from docx import Document
from PIL import Image
import io
import re
import logging
import sqlite3

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  



def clean_text(text: str) -> str:
    text = text.replace('\x0c', ' ')       # remove form feed characters (from PDFs)
    text = re.sub(r'\s+', ' ', text)       # normalize whitespace
    text = re.sub(r'<[^>]+>', '', text)    # remove HTML tags
    text = text.strip()
    return text


def load_db(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    text_data = ""
    for table_name in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"):
        table = table_name[0]
        rows = cursor.execute(f"SELECT * FROM {table}").fetchall()
        text_data += f"\nTable: {table}\n"
        text_data += "\n".join([str(row) for row in rows])
    conn.close()
    return text_data


def load_pdf(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def load_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_csv(path):
    df = pd.read_csv(path)
    return df.to_string()

# def load_image(path):
#     image = Image.open(path)
#     text = pytesseract.image_to_string(image)
#     print("OCR extracted text:\n", text)
#     return text



def load_image(upload_file):
    """Handles image UploadFile from FastAPI correctly"""
    try:
        image = Image.open(io.BytesIO(upload_file.file.read()))
        text = pytesseract.image_to_string(image)
        # print("\n===== OCR Extracted Text =====")
        # print(text)
        # print("===== END =====\n")
        return clean_text(text)
    except Exception as e:
        raise RuntimeError(f"Image processing failed: {e}")

def load_file(path):
    path= path.lower()
    if path.endswith(".pdf"): return load_pdf(path)
    elif path.endswith(".docx"): return load_docx(path)
    elif path.endswith(".txt"): return load_txt(path)
    elif path.endswith(".csv"): return load_csv(path)
    elif path.lower().endswith((".jpg", ".png","jpeg")): return load_image(path)
    elif path.endswith(".db"): return load_db(path)

    else: raise Exception("Unsupported file format")