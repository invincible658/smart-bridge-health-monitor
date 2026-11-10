"""
ChromaDB Vector Indexing Module for Smart Bridge Structural Health Monitoring.
Indexes:
1. Z24 SIMCES progressive damage ground-truth benchmark logs (rag/data/damage_ground_truth.json)
2. IRC-SP-35 & FHWA civil bridge inspection maintenance standards (rag/data/inspection_standards.json)
Using sentence-transformers all-MiniLM-L6-v2 embeddings.
"""
import os
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

RAG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag")
DATA_DIR = os.path.join(RAG_DIR, "data")
CHROMA_PERSIST_DIR = os.path.join(RAG_DIR, "chroma_db")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def get_embedding_function():
    """Returns local HuggingFace sentence transformer embedding function."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def load_knowledge_base_documents() -> list[Document]:
    """
    Parses both damage_ground_truth.json and inspection_standards.json
    into a unified list of LangChain Document objects.
    """
    docs = []
    
    # 1. Load Z24 Progressive Damage Ground Truth Logs
    damage_file = os.path.join(DATA_DIR, "damage_ground_truth.json")
    if os.path.exists(damage_file):
        with open(damage_file, "r", encoding="utf-8") as f:
            scenarios = json.load(f)
            for item in scenarios:
                content = (
                    f"Structural Damage Scenario: {item['damage_type']} (Scenario ID: {item['scenario_id']})\n"
                    f"Description: {item['description']}\n"
                    f"Affected Components: {item['affected_elements']}\n"
                    f"Modal & Vibration Indicators: {item['modal_indicators']}\n"
                    f"Severity Level: {item['severity']}"
                )
                docs.append(Document(
                    page_content=content,
                    metadata={"source": "Z24_SIMCES", "scenario_id": item["scenario_id"], "type": "damage_ground_truth"}
                ))
                
    # 2. Load IRC-SP-35 & FHWA Inspection Protocols
    standards_file = os.path.join(DATA_DIR, "inspection_standards.json")
    if os.path.exists(standards_file):
        with open(standards_file, "r", encoding="utf-8") as f:
            standards = json.load(f)
            for item in standards:
                content = (
                    f"Civil Standard: {item['standard_title']} (Ref: {item['standard_id']})\n"
                    f"Trigger Condition: {item['trigger_condition']}\n"
                    f"Mandatory Inspection Protocol: {item['inspection_protocol']}\n"
                    f"Mandatory Corrective Action: {item['corrective_actions']}"
                )
                docs.append(Document(
                    page_content=content,
                    metadata={"source": item["standard_id"], "type": "inspection_standard"}
                ))
                
    return docs

def build_or_load_vector_db(persist_directory: str = None) -> Chroma:
    """
    Initializes ChromaDB vector store. If not already built, indexes the knowledge base documents.
    """
    target_dir = persist_directory or CHROMA_PERSIST_DIR
    embeddings = get_embedding_function()
    
    # Check if database already exists
    if os.path.exists(target_dir) and len(os.listdir(target_dir)) > 0:
        db = Chroma(
            collection_name="bridge_knowledge_base",
            embedding_function=embeddings,
            persist_directory=target_dir
        )
        return db
        
    # Otherwise, build from scratch
    docs = load_knowledge_base_documents()
    if not docs:
        raise FileNotFoundError(f"Knowledge base JSON files not found in '{DATA_DIR}'.")
        
    os.makedirs(target_dir, exist_ok=True)
    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="bridge_knowledge_base",
        persist_directory=target_dir
    )
    return db

def retrieve_similar_contexts(query: str, k: int = 2, persist_directory: str = None) -> list[Document]:
    """
    Queries ChromaDB and retrieves top-k relevant benchmark cases and standards.
    """
    db = build_or_load_vector_db(persist_directory=persist_directory)
    return db.similarity_search(query, k=k)
