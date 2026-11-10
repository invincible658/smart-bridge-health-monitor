"""
RAG-based engineering incident advisory generator using Groq / Gemini LLMs.
"""
import os
from langchain_groq import ChatGroq

def draft_incident_advisory(anomaly_details: dict, context_docs: list, groq_api_key: str = None) -> str:
    key = groq_api_key or os.getenv("GROQ_API_KEY")
    if not key:
        return "GROQ_API_KEY not configured. Please supply an API key in .env"
    
    llm = ChatGroq(temperature=0.2, groq_api_key=key, model_name="llama-3.3-70b-versatile")
    context_text = "\n---\n".join([doc.page_content for doc in context_docs])
    
    prompt = f"""
    You are an expert Structural Health Informatics Assistant. A bridge anomaly has been detected.
    
    ANOMALY METRICS:
    {anomaly_details}
    
    HISTORICAL BENCHMARK INCIDENTS:
    {context_text}
    
    Write an actionable, professional 3-paragraph inspection advisory for civil engineers.
    """
    res = llm.invoke(prompt)
    return res.content
