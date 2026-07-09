import os
import sys

# Ensure project root is in python path so imports don't break
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Absolute path resolutions
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF_PATH = os.path.join(BASE_DIR, "data", "docs", "who_amr_guideline.pdf")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "data", "vector_db")

def run_rag_ingestion():
    print("\n [START] Initializing WHO AMR Guidelines PDF Ingestion...")
    
    # 1. Guard Clauses
    if not os.path.exists(PDF_PATH):
        print(f"Error: Source PDF missing at: {PDF_PATH}")
        print("Please ensure the WHO PDF is placed in your data/docs/ directory.")
        return

    try:
        # 2. Extract Document Text
        print(" Extracting text layers from PDF via PyPDF...")
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()
        print(f"   → Loaded {len(documents)} raw document pages.")

        # 3. Contextual Text Chunking
        print(" Chunking document text (Size: 1000 tokens, Overlap: 200)...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)
        print(f"   → Created {len(chunks)} overlapping text segments.")

        # 4. Generate Embeddings & Compile Vector Store
        print(" Connecting to OpenAI Embeddings API Engine...")
        # Note: Enforces the use of your environment's OPENAI_API_KEY
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        print(" Indexing matrix into local FAISS Vector Store...")
        vector_db = FAISS.from_documents(chunks, embeddings)

        # 5. Serialize Index to Disk
        os.makedirs(VECTOR_DB_DIR, exist_ok=True)
        vector_db.save_local(VECTOR_DB_DIR)
        print(f" [SUCCESS] Vector index serialized cleanly to: {VECTOR_DB_DIR}\n")

    except Exception as e:
        print(f" Critical Ingestion Failure: {str(e)}")

if __name__ == "__main__":
    run_rag_ingestion()