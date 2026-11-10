"""
Unit tests for Phase 3:
- Knowledge base JSON parsing
- ChromaDB vector store indexing & similarity retrieval
- RAG incident advisory generation (with offline synthesis fallback)
"""
import os
import gc
import shutil
import tempfile
import pytest

from src.rag_indexer import load_knowledge_base_documents, build_or_load_vector_db, retrieve_similar_contexts
from src.report_generator import generate_incident_advisory, answer_inspector_query

def test_load_knowledge_base_documents():
    docs = load_knowledge_base_documents()
    assert len(docs) >= 15  # 11 Z24 damage logs + 4 civil standards
    
    # Check document metadata
    has_damage = any(d.metadata.get("type") == "damage_ground_truth" for d in docs)
    has_standard = any(d.metadata.get("type") == "inspection_standard" for d in docs)
    
    assert has_damage
    assert has_standard

def test_chroma_indexing_and_retrieval():
    temp_chroma = tempfile.mkdtemp()
    try:
        # Build vector store in temp directory
        db = build_or_load_vector_db(persist_directory=temp_chroma)
        assert db is not None
        
        # Test semantic search for pier settlement
        query = "differential pier settlement bearing failure"
        results = retrieve_similar_contexts(query, k=2, persist_directory=temp_chroma)
        
        assert len(results) == 2
        top_text = results[0].page_content.lower()
        # Should match pier settlement or bearing inspection standards
        assert "settlement" in top_text or "pier" in top_text or "bearing" in top_text
        
        # Explicitly release handles for Windows SQLite/Chroma file locks
        del db
        del results
        gc.collect()
    finally:
        # ignore_errors=True handles any remaining Windows background file locks safely
        shutil.rmtree(temp_chroma, ignore_errors=True)

def test_advisory_generation_offline():
    # Test generation without API keys (verifies offline template synthesis)
    res = generate_incident_advisory(
        segment_id=450,
        anomaly_score=-0.42,
        shap_summary="- ch14_dominant_freq: attribution score +0.48\n- ch15_kurtosis: attribution score +0.26",
        top_channels=[14, 15],
        forecast_warning="Critical threshold breach predicted in 5 steps"
    )
    
    assert "advisory_text" in res
    assert len(res["advisory_text"]) > 100
    assert "Segment #450" in res["advisory_text"]
    assert "IRC-SP-35" in res["advisory_text"] or "Z24" in res["advisory_text"]
