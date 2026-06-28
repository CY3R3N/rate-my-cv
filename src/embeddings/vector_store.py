# src/embeddings/vector_store.py

from langchain_community.vectorstores import FAISS

def build_vector_store(chunks: list[str], embedder):
    """Embed all chunks and store them in a FAISS index."""
    
    vector_store = FAISS.from_texts(chunks, embedder)
    return vector_store


def search_vector_store(vector_store, query: str, k: int = 4):
    """Search the vector store for the most relevant chunks."""
    
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]