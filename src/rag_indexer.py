"""
ChromaDB indexer:
Indexes known historical bridge damage benchmark events using sentence-transformers MiniLM.
"""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_chroma_db(persist_directory: str = "./rag/chroma_db"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        collection_name="bridge_incidents",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    return db
