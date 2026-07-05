import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Initialize local embedding model and DB connection
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def process_and_index_pdf(pdf_path: str, user_id: str):
    """Parses, chunks, and injects a PDF into ChromaDB tagged by user_id."""
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    
    for chunk in chunks:
        chunk.metadata["user_id"] = user_id
        chunk.metadata["source"] = os.path.basename(pdf_path)
        
    vectorstore.add_documents(chunks)
    return len(chunks)
import time

# Try to initialize embeddings with a brief retry loop for network hiccups
print("Initializing embedding model...")
for attempt in range(3):
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            # This kwargs dictionary passes directly to sentence-transformers
            model_kwargs={'device': 'cpu'} 
        )
        print("Embedding model loaded successfully.")
        break
    except Exception as e:
        print(f"Network glitch on attempt {attempt+1}... retrying in 2 seconds.")
        time.sleep(2)
        if attempt == 2:
            raise e # If it fails 3 times, let it crash so we can see the error