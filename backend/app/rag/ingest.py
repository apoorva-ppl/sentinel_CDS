import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DOCS_PATH = os.path.join(backend_root, "data", "docs", "who_amr_guidelines.pdf")
CHROMA_PATH = os.path.join(backend_root, "chroma_db")

def ingest_documents():
    # 1. Load PDF
    loader = PyPDFLoader(DOCS_PATH)
    documents = loader.load()

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    # 3. Embed and store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    print(f" Ingested {len(chunks)} chunks from WHO AMR Guidelines into ChromaDB")
    return vectorstore

if __name__ == "__main__":
    ingest_documents()