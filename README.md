# 🌉 Smart Bridge Health Monitoring System
### Real-Time Vibration Telemetry, Machine Learning Anomaly Detection, Time-Series Forecasting & Explainable AI

An automated end-to-end Structural Health Monitoring (SHM) full-stack web platform built for civil engineers. The system continuously analyzes multi-sensor vibration telemetry from the benchmark Z24 Bridge dataset, detects instantaneous anomalies using **Isolation Forest**, forecasts long-term structural stiffness degradation using **ARIMA**, explains detected faults via **SHAP**, and synthesizes plain-English maintenance advisories using a **Retrieval-Augmented Generation (RAG)** pipeline powered by **ChromaDB** and modern LLMs (Groq / Gemini).

---

## 🚀 Key Features

- **Benchmark Dataset:** Ingests the real-world **Z24 Bridge dataset** from Hugging Face (`thanglexuan/Z24-dataset-processed`) with 27-channel accelerometer recordings sampled at 100 Hz.
- **Digital Signal Processing (DSP):** Removes static sensor drift via DC detrending and attenuates high-frequency electrical noise using a 4th-order Butterworth low-pass filter (30 Hz cutoff).
- **Physics-Informed Feature Engineering:** Calculates time-domain metrics (RMS, peak-to-peak, kurtosis, skewness) and FFT frequency-domain metrics (dominant mode frequency, spectral entropy).
- **Dual-Engine Modeling:**
  - **Isolation Forest:** Evaluates incoming segments against undamaged baseline signals to detect sudden damage/cracking.
  - **ARIMA Time-Series Forecasting:** Tracks modal frequency degradation trends over time to forecast safety threshold breaches before failure occurs.
- **Explainable AI (XAI):** Uses SHAP (SHapley Additive Explanations) TreeExplainer to break down which specific sensor channels and vibration features triggered an alert.
- **RAG Engineering Advisory Engine:** Combines curated Z24 SIMCES ground-truth damage logs and IRC-SP-35 / FHWA civil maintenance guidelines in **ChromaDB** using `all-MiniLM-L6-v2` embeddings to generate grounded incident reports via Groq (Llama 3.3) or Gemini.
- **Modern Full-Stack Dashboard:**
  - **Backend:** FastAPI REST API providing streaming telemetry, detection, forecasting, and Q&A endpoints.
  - **Frontend:** React (Vite) + Tailwind CSS + Lucide Icons + Recharts with interactive waveforms, risk gauges, ARIMA forecast curves, SHAP waterfall plots, and an interactive AI Inspector chat.

---

## 📁 Repository Structure

```text
bridge-health/
│
├── README.md                     # Main repository landing guide
├── requirements.txt              # Python backend dependencies
├── .gitignore                    # Git ignore rules (node_modules, models, cache, secrets)
│
├── data/
│   ├── download_z24.py           # Script to fetch/cache Z24 from Hugging Face
│   └── cache/                    # Local cached arrays (git-ignored)
│
├── src/                          # Core modular DSP, ML & Time-Series library
│   ├── __init__.py
│   ├── dataset_loader.py         # Hugging Face Z24 loader & scenario splitting
│   ├── preprocessing.py          # Detrending, Butterworth filtering, normalization
│   ├── features.py               # Time-domain & FFT frequency feature extraction
│   ├── train.py                  # Isolation Forest model training
│   ├── forecast.py               # ARIMA time-series degradation forecaster
│   ├── evaluate.py               # ROC-AUC and precision-recall evaluation
│   ├── explain.py                # SHAP attribution engine
│   ├── rag_indexer.py            # ChromaDB incident indexing with MiniLM
│   └── report_generator.py       # LangChain + Gemini/Groq incident reporter
│
├── rag/                          # Retrieval-Augmented Generation Knowledge Base
│   ├── data/
│   │   ├── damage_ground_truth.json   # 11 Curated Z24 progressive damage logs
│   │   └── inspection_standards.json  # IRC-SP-35 & FHWA bridge maintenance protocols
│   └── chroma_db/                # Local persistent vector database (git-ignored)
│
├── backend/                      # FastAPI Backend Application
│   ├── main.py                   # FastAPI server entry point & CORS configuration
│   └── routes/                   # REST API routers
│       ├── __init__.py
│       ├── telemetry.py          # /api/telemetry (Waveform & spectrum streaming)
│       ├── detection.py          # /api/detect & /api/detect/explain (Isolation Forest & SHAP)
│       ├── forecasting.py        # /api/forecast (ARIMA degradation curves)
│       └── advisory.py           # /api/advisory & /api/advisory/chat (RAG & LLM Q&A)
│
├── frontend/                     # React (Vite) + Tailwind CSS Dashboard
│   ├── package.json              # Node dependencies (React 18, Recharts, Lucide, Axios)
│   ├── vite.config.js            # Vite bundler & API reverse-proxy configuration
│   ├── tailwind.config.js        # Tailwind CSS theme styling
│   ├── postcss.config.js         # PostCSS configuration
│   ├── index.html                # Application HTML entry point
│   └── src/
│       ├── main.jsx              # React DOM mounting
│       ├── App.jsx               # Main executive monitoring layout
│       ├── index.css             # Tailwind base & custom directives
│       └── components/           # Modular dashboard UI widgets
│           ├── TelemetryChart.jsx# Real-time multi-channel vibration waveform plot
│           ├── AnomalyGauge.jsx  # Color-coded anomaly risk score meter
│           ├── ForecastChart.jsx # ARIMA stiffness forecast with critical threshold line
│           ├── ShapBar.jsx       # Horizontal SHAP feature contribution bar chart
│           └── AiChat.jsx        # Interactive AI Civil Inspector console
│
├── models/                       # Trained model binaries (git-ignored)
│   └── .gitkeep
│
└── tests/                        # Automated unit testing suite
    ├── __init__.py
    ├── test_preprocessing.py     # Signal filtering & detrending tests
    ├── test_features.py          # Statistical & FFT feature extraction tests
    └── test_model.py             # Isolation Forest training & inference tests
```

---

## 🛠️ Quickstart Guide

### 1. Backend Setup & Dependencies
```bash
# Clone the repository
git clone https://github.com/<your-username>/bridge-health.git
cd bridge-health

# Create and activate Python virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Keys
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Start the FastAPI Backend
```bash
uvicorn backend.main:app --reload --port 8000
```
*API interactive documentation will be live at `http://localhost:8000/docs`.*

### 4. Start the React Frontend Dashboard
In a separate terminal window:
```bash
cd frontend

# Install node packages
npm install

# Run Vite development server
npm run dev
```
*Dashboard will be available at `http://localhost:5173`.*

---

## 🧪 Running Unit Tests
```bash
pytest tests/ -v
```

---

## 📜 Civil Standards & Ground Truth References
- **Z24 Benchmark:** KU Leuven Department of Civil Engineering (SIMCES Project BE-3157).
- **Inspection Standard:** Indian Roads Congress (*IRC-SP-35: Guidelines for Inspection and Maintenance of Bridges*).
- **Federal Standard:** Federal Highway Administration (*FHWA Bridge Inspector's Reference Manual*).
