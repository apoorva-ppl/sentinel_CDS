import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
CHROMA_PATH = os.path.join(backend_root, "chroma_db")

# Load once at module level
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

try:
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
except Exception as e:
    print(f"ChromaDB not loaded: {e}")
    retriever = None

def get_copilot_response(message: str, patient_context: dict) -> str:
    # 1. Retrieve relevant AMR guidelines
    medical_context = ""
    if retriever:
        docs = retriever.invoke(message)
        medical_context = "\n".join([doc.page_content for doc in docs])

    # 2. Build prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are Sentinel, a clinical AI copilot for antimicrobial resistance.
        
Patient Context: {patient_context}
Relevant Guidelines: {medical_context}

Answer clinically. Be concise. Never hallucinate drug names."""),
        ("human", "{message}")
    ])

    # 3. Call Groq
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY")
    )

    chain = prompt | llm
    response = chain.invoke({
        "patient_context": str(patient_context),
        "medical_context": medical_context,
        "message": message
    })

    return response.content