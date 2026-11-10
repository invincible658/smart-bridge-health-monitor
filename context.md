# Project Context: Smart Bridge Health Monitoring System

## 1. Project Background & Objective
- **Problem:** India has 1.72 lakh+ bridges. Conventional manual inspections are infrequent, expensive, subjective, and slow, creating risks of undetected catastrophic structural failures (e.g., Morbi bridge collapse).
- **Goal:** Build an end-to-end, software-based Structural Health Monitoring (SHM) system that continuously analyzes bridge vibration telemetry, detects structural anomalies via unsupervised Machine Learning (Isolation Forest), forecasts temporal structural degradation trends (ARIMA), explains alerts using game-theoretic feature attribution (SHAP), and generates plain-English engineering incident reports using a Retrieval-Augmented Generation (RAG) pipeline paired with a modern React + FastAPI web application.
- **Academic Context:** 3rd Year B.Sc. Data Science Minor Project, SPPU Pune.
- **Student Profile (Nakul):** Strong Python, SQL, OOP, Pandas pipelines, Scikit-learn (clustering/anomaly detection), Time-Series Modeling (ARIMA/SARIMA), GenAI/RAG stack (LangChain, ChromaDB, Sentence-Transformers MiniLM, Groq/Gemini APIs), and Full-Stack Web Development (FastAPI + React + Tailwind CSS).

---

## 2. Dataset: Z24 Bridge Benchmark (Hugging Face)
- **Source:** Hugging Face repository `thanglexuan/Z24-dataset-processed` (or mirror `Vishwaraj9659/Z24-dataset-processed-bucket`).
- **Nature of Data:** Real-world vibration response data recorded from a full-scale prestressed concrete box-girder highway bridge in Bern/Solothurn, Switzerland, prior to its planned demolition.
- **Data Dimensions:** Array shaped `(1530, 27, 6000)`:
  - `1530` segments = 17 damage scenarios × 9 setup sweeps × 10 test windows.
  - `27` channels = Accelerometer vibration sensors distributed along deck and piers.
  - `6000` time samples = 60-second continuous recording at 100 Hz per window.
- **Scenarios & Ground Truth Split:**
  - **Scenarios 0–4:** Undamaged healthy baseline under varying environmental conditions. Used exclusively for **training** the unsupervised model.
  - **Scenarios 5–16:** Real progressive physical structural damage (Pier lowering 20mm-95mm, foundation tilt, spalling of concrete 12m²-24m², concrete hinge failure, anchor head failures, rupture of 2 to 6 tendons). Used as the **anomaly evaluation test set**.

---

## 3. Signal Pre-processing Requirements
Even though pre-segmented, the raw signals require domain-specific digital signal processing:
1. **Detrending & DC Bias Removal:** Multi-channel accelerometers experience drift and static offsets; `scipy.signal.detrend` removes DC components.
2. **Digital Low-Pass Filtering:** A 4th-order Butterworth filter (cutoff = 30 Hz) eliminates high-frequency sensor/electrical noise, retaining critical structural modal dynamics (0.5 Hz – 30 Hz).
3. **Z-score Standardization:** Normalizes the 27 channels relative to the baseline so high-amplitude sensors do not disproportionately bias the feature extractors.

---

## 4. End-to-End System Components
1. **Data Ingestion (`src/dataset_loader.py`):** Loads Z24 dataset via `datasets.load_dataset()`, assigns normal vs. damage labels based on scenario IDs.
2. **Preprocessing (`src/preprocessing.py`):** Detrends, filters (Butterworth low-pass 30 Hz), and standardizes array segments.
3. **Feature Extraction (`src/features.py`):** Extracts per-channel time-domain (RMS, peak-to-peak, kurtosis, skewness) and FFT frequency-domain metrics (dominant frequency, spectral entropy, PSD energy).
4. **Dual Detection & Forecasting Engine:**
   - **Point Anomaly Detection (`src/train.py`, `src/evaluate.py`):** Trains Isolation Forest on undamaged baseline; evaluates using ROC-AUC (target $\ge 0.85$) and precision-recall on progressive damage scenarios.
   - **Time-Series Forecasting (`src/forecast.py`):** Fits ARIMA on sequential modal frequencies across scenarios to track gradual stiffness decline and forecast threshold breaches.
5. **Explainable AI (`src/explain.py`):** Employs SHAP TreeExplainer to attribute anomaly scores to individual sensor channels and vibration frequencies.
6. **RAG Knowledge Base & Reporter (`src/rag_indexer.py`, `src/report_generator.py`):** 
   - **Knowledge Base:** Curated JSON/Markdown knowledge base of Z24 SIMCES ground-truth damage logs + IRC-SP-35 / Federal Highway bridge inspection guidelines indexed in ChromaDB.
   - **Retrieval & LLM:** Queries matching historical cases with top SHAP features and prompts Groq (Llama 3.3) / Gemini to draft a structured incident advisory.
7. **Web Application (`backend/` & `frontend/`):**
   - **Backend:** FastAPI REST endpoints (`/api/telemetry`, `/api/detect`, `/api/forecast`, `/api/explain`, `/api/advisory`, `/api/chat`).
   - **Frontend:** React (Vite) + Tailwind CSS + Lucide Icons + Recharts for interactive waveforms, anomaly gauges, ARIMA forecast curves, SHAP waterfall plots, and AI inspection chat.
