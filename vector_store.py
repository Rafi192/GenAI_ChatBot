import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
doc_chunks = []

def embed_and_store(text, metadata):
    global doc_chunks
    chunks = [text[i:i+500] for i in range(0, len(text), 400)]
    vectors = model.encode(chunks)
    index.add(np.array(vectors))
    doc_chunks.extend([(chunk, metadata) for chunk in chunks])

def search_similar(query):
    q_vec = model.encode([query])
    D, I = index.search(np.array(q_vec), k=3)
    
    # Handle no results
    if I[0].size == 0 or I[0][0] == -1:
        return []
    
    return [doc_chunks[i] for i in I[0] if i < len(doc_chunks)]



