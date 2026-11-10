"""
RAG-Powered Civil Engineering Incident Report Generator.
Synthesizes:
1. Instantaneous Anomaly Detection metrics (Isolation Forest score)
2. SHAP diagnostic attribution (channels & frequencies)
3. ARIMA degradation forecast projection
4. Retrieved historical damage benchmarks & IRC-SP-35 / FHWA safety standards
To generate an actionable, professional 3-paragraph inspection advisory using Groq / Gemini LLMs.
"""
import os
from dotenv import load_dotenv
from src.rag_indexer import retrieve_similar_contexts

load_dotenv()

def generate_incident_advisory(
    segment_id: int,
    anomaly_score: float,
    shap_summary: str,
    top_channels: list,
    forecast_warning: str = None,
    groq_api_key: str = None,
    gemini_api_key: str = None
) -> dict:
    """
    Generates a structured inspection advisory for detected structural deviations.
    """
    channels_str = ", ".join([f"Channel {c}" for c in top_channels]) if top_channels else "Multiple deck channels"
    
    # 1. Formulate semantic query for ChromaDB
    query = (
        f"Structural anomaly detected on {channels_str}. "
        f"Contributing signals: {shap_summary}. "
        f"Forecast projection: {forecast_warning or 'Stiffness decline'}."
    )
    
    # 2. Retrieve top 2 contextual records from ChromaDB
    retrieved_docs = retrieve_similar_contexts(query, k=2)
    context_text = "\n---\n".join([doc.page_content for doc in retrieved_docs])
    
    matched_scenario = "Historical Benchmark Failure Scenario"
    for doc in retrieved_docs:
        if doc.metadata.get("type") == "damage_ground_truth":
            matched_scenario = doc.page_content.split("\n")[0]
            break
            
    # 3. Check for available LLM API keys
    key_groq = groq_api_key or os.getenv("GROQ_API_KEY")
    key_gemini = gemini_api_key or os.getenv("GEMINI_API_KEY")
    
    prompt = f"""You are a Lead Structural Health Informatics Engineer advising a highway maintenance team.
A sensor anomaly alert has been triggered on the bridge monitoring network.

TELEMETRY & MODEL DIAGNOSTICS:
- Segment ID: #{segment_id}
- Anomaly Decision Risk Score: {anomaly_score:.3f} (Safety Baseline Threshold: 0.00)
- Primary Affected Channels: {channels_str}
- Forecast Projection: {forecast_warning or 'No critical threshold breach predicted in next 14 steps.'}
- Top Contributing Signals (SHAP Attribution):
{shap_summary}

HISTORICAL BENCHMARKS & CIVIL MAINTENANCE STANDARDS RETRIEVED:
{context_text}

TASK:
Write a concise, professional 3-paragraph engineering incident advisory:
Paragraph 1: Executive Summary - State what was detected, severity, and the primary sensor channels involved.
Paragraph 2: Physical Interpretation - Relate the frequency shifts/kurtosis to physical damage (e.g., differential pier settlement, bearing wear, or tendon loss) based on the retrieved benchmark cases.
Paragraph 3: Recommended Action Plan - Prescribe immediate operational procedures (e.g., traffic speed restrictions, visual bearing checks, level surveying) in compliance with the retrieved standards.
"""

    advisory_text = None

    # Try Groq (Llama 3.3) first if configured
    if key_groq:
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(temperature=0.2, groq_api_key=key_groq, model_name="llama-3.3-70b-versatile")
            response = llm.invoke(prompt)
            advisory_text = response.content
        except Exception as e:
            print(f"[!] Groq inference failed ({e}), checking fallback...")

    # Fallback to Gemini if configured
    if not advisory_text and key_gemini:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(temperature=0.2, google_api_key=key_gemini, model="gemini-1.5-flash")
            response = llm.invoke(prompt)
            advisory_text = response.content
        except Exception as e:
            print(f"[!] Gemini inference failed ({e}), using rule-based synthesis.")

    # Graceful offline template if no LLM key is set
    if not advisory_text:
        advisory_text = (
            f"Anomalous vibration telemetry flagged at Segment #{segment_id} with an anomaly risk score of {anomaly_score:.3f}. "
            f"Primary deviation isolated on {channels_str} driven by {shap_summary.replace(chr(10), '; ')}.\n\n"
            f"Comparison with historical Z24 benchmark logs correlates this behavior with {matched_scenario}. "
            f"The modal frequency and strain variations indicate localized stiffness reduction across intermediate structural elements.\n\n"
            f"In accordance with IRC-SP-35 / FHWA maintenance guidelines, schedule an urgent visual bearing and alignment inspection "
            f"within 24 hours. Implement temporary traffic speed restrictions to minimize dynamic impact load while level surveying tracks potential foundation movement."
        )

    return {
        "segment_id": segment_id,
        "anomaly_score": float(anomaly_score),
        "matched_benchmark": matched_scenario,
        "retrieved_context": [doc.page_content for doc in retrieved_docs],
        "advisory_text": advisory_text
    }

def answer_inspector_query(query: str, groq_api_key: str = None) -> str:
    """
    Answers natural language questions asked by engineers via the frontend chat console.
    """
    retrieved = retrieve_similar_contexts(query, k=2)
    context_text = "\n---\n".join([d.page_content for d in retrieved])
    
    key = groq_api_key or os.getenv("GROQ_API_KEY")
    if key:
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(temperature=0.3, groq_api_key=key, model_name="llama-3.3-70b-versatile")
            prompt = f"Use the bridge knowledge base below to answer the engineer's question clearly:\n\nCONTEXT:\n{context_text}\n\nQUESTION: {query}"
            return llm.invoke(prompt).content
        except Exception:
            pass
            
    # Offline response
    return f"Based on archived standards (IRC-SP-35 / Z24 benchmark): '{retrieved[0].page_content.splitlines()[0]}' - consult structural inspection manual for detailed tolerances."
