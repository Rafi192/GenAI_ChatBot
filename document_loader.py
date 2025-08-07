import pdfplumber, pytesseract, pandas as pd
from docx import Document
from PIL import Image

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

def load_image(path):
    image = Image.open(path)
    return pytesseract.image_to_string(image)

def load_file(path):
    if path.endswith(".pdf"): return load_pdf(path)
    elif path.endswith(".docx"): return load_docx(path)
    elif path.endswith(".txt"): return load_txt(path)
    elif path.endswith(".csv"): return load_csv(path)
    elif path.lower().endswith((".jpg", ".png")): return load_image(path)
    else: raise Exception("Unsupported file format")