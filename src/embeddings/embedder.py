# src/embeddings/embedder.py

from langchain_huggingface import HuggingFaceEmbeddings

def load_embedder():
    """Load the HuggingFace embedding model."""
    
    embedder = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embedder