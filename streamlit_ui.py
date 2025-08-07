import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("📚 RAG Chatbot Interface")

# Upload section
st.header("📤 Upload a File")
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "csv", "jpg", "png", "db"])

if uploaded_file:
    with st.spinner("Uploading and processing..."):
        files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post("http://127.0.0.1:8000/upload", files=files)
        if response.status_code == 200:
            st.success("✅ File uploaded and indexed.")
        else:
            st.error("❌ Upload failed.")

# Query section
st.header("❓ Ask a Question")
question = st.text_input("Type your question:")

if question:
    with st.spinner("Querying the knowledge base..."):
        payload = {"question": question}
        response = requests.post("http://127.0.0.1:8000/query", json=payload)

        if response.status_code == 200:
            data = response.json()
            st.subheader("Answer:")
            st.success(data["answer"])
            st.subheader("Context:")
            st.code(data["context"])
            st.markdown("**Sources:** " + ", ".join(data["sources"]))
        else:
            st.error("Failed to get a response.")
