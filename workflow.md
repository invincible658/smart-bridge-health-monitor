# Development Workflow & Execution Guide

## 1. Step-by-Step Implementation Workflow

```
[Phase 1: Ingestion & DSP] ──▶ [Phase 2: Feature Engineering] ──▶ [Phase 3: Dual Models (Isolation Forest + ARIMA) & SHAP]
                                                                                               │
                                                                                               ▼
[Phase 5: React Web UI] ◀── [FastAPI REST API] ◀── [Phase 4: ChromaDB RAG Knowledge Base] ◀───┘
```

### Phase 1: Ingestion & Pre-processing (`src/dataset_loader.py`, `src/preprocessing.py`)
1. Stream/download the processed Z24 dataset via `datasets.load_dataset("thanglexuan/Z24-dataset-processed")`.
2. Extract the data array `X` of shape `(1530, 27, 6000)` and scenario labels `scenario_id`.
3. Construct the training split:
   - Normal baseline training data: `scenario_id in [0, 1, 2, 3, 4]`.
   - Test data: Both healthy and progressive damage scenarios `[5..16]`.
4. Apply the DSP filter pipe on each window:
   - `detrend(signal)` to remove DC static bias.
   - 4th-order Butterworth low-pass filter at 30 Hz cutoff.
   - Standardize channel amplitudes: `(sig - mean) / std`.

### Phase 2: Feature Engineering (`src/features.py`)
1. Compute time-domain metrics per channel:
   - Root Mean Square (RMS): $\sqrt{\frac{1}{N}\sum x_i^2}$
   - Peak-to-Peak (PTP): $\max(x) - \min(x)$
   - Kurtosis & Skewness.
2. Compute frequency-domain metrics via real FFT (`scipy.fft.rfft`):
   - Dominant frequency: $\arg\max |FFT(f)|$ (excluding DC 0 Hz).
   - Spectral entropy: measure of disorder in the Power Spectral Density (PSD).
3. Assemble into a tabular feature matrix `(1530 samples, 27 * n_features)`.

### Phase 3: Dual Model Training & Diagnostics (`src/train.py`, `src/forecast.py`, `src/explain.py`)
1. **Isolation Forest (Point Anomaly):**
   - Fit `StandardScaler` on the normal training features only.
   - Train `IsolationForest(n_estimators=200, contamination=0.05, random_state=42)`.
   - Evaluate on the test set using `roc_auc_score` and precision-recall metrics (target: ROC-AUC $\ge 0.85$).
   - Save artifacts to `models/isolation_forest.pkl` and `models/scaler.pkl`.
2. **ARIMA (Degradation Forecasting):**
   - Fit `ARIMA(p, d, q)` on sequential dominant frequencies across time.
   - Forecast future modal frequency trajectory (14 to 30 steps ahead) with 95% confidence intervals.
   - Trigger predictive warning if projected curve crosses safety threshold ($< 3.5 \text{ Hz}$).
3. **SHAP Diagnostics:**
   - Initialize `shap.TreeExplainer(model)` on scaled features.
   - Extract the top 5 sensor/frequency culprits for any flagged segment for diagnosis.

### Phase 4: Vector Indexing & RAG Reporting (`src/rag_indexer.py`, `src/report_generator.py`)
1. Structure the knowledge base in `rag/data/damage_ground_truth.json` (compiled from official Z24 SIMCES research papers detailing the 17 progressive damage stages) and `rag/data/inspection_standards.json` (IRC-SP-35 / FHWA maintenance guidelines).
2. Embed the knowledge base documents using `all-MiniLM-L6-v2` and index them into `ChromaDB` (`rag/chroma_db`).
3. On anomaly detection or forecast breach, formulate a semantic query based on the top SHAP features and predicted degradation.
4. Retrieve matching historical structural incidents from ChromaDB.
5. Invoke Groq (Llama 3.3) or Gemini LLM to draft a concise 3-paragraph inspection advisory.

### Phase 5: FastAPI Backend & React Frontend (`backend/`, `frontend/`)
1. **FastAPI Endpoints (`backend/main.py`):**
   - `GET /api/telemetry?segment_id=X`: Returns 27-channel time-series vibration slice and FFT spectrum.
   - `POST /api/detect`: Preprocesses signal and computes Isolation Forest anomaly risk score.
   - `GET /api/forecast`: Returns ARIMA frequency forecast curve and safety threshold bounds.
   - `POST /api/explain`: Computes SHAP values and returns top contributing channels/frequencies.
   - `POST /api/advisory`: Queries ChromaDB RAG and generates LLM inspection briefing.
   - `POST /api/chat`: Handles user queries from the frontend AI chat assistant.
2. **React + Tailwind Frontend (`frontend/src/`):**
   - **Telemetry View:** Interactive multi-channel waveform plots using Recharts.
   - **Health Monitor Gauge:** Color-coded alert meter (Green = Healthy, Yellow = Warning, Red = Critical).
   - **ARIMA Forecast Horizon:** Line chart with confidence bands showing projected stiffness degradation.
   - **SHAP Diagnostics:** Waterfall bar chart showing which channels drove the anomaly score.
   - **AI Inspector Chat:** Interactive assistant to review incident reports and ask natural language questions.

---

## 2. Instructions for Next LLM Agent / Developer
1. **Always read `context.md`** to verify data shapes, split criteria, and scientific constraints.
2. **Check `techstack.md`** before writing imports or installing dependencies.
3. **Follow the modular design** specified in `workflow.md`:
   - Keep ML, time-series forecasting, and signal processing inside `src/`.
   - Expose REST API routes inside `backend/`.
   - Keep UI components inside `frontend/`.
4. **Follow `CLAUDE.md` guidelines:** Think before coding, keep it simple, make surgical changes, and verify goals.
5. **Never hardcode secrets**: Read `GROQ_API_KEY` or `GEMINI_API_KEY` via `os.getenv()`.
