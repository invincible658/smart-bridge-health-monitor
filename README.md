# 🌉 Smart Bridge Health Monitoring System
### Machine Learning & Explainable AI for Structural Health Monitoring

An automated structural health monitoring (SHM) software system that continuously analyzes multi-channel vibration telemetry, detects anomalies using unsupervised machine learning (Isolation Forest), explains alerts via SHAP feature attribution, and generates plain-English engineering advisories using a Retrieval-Augmented Generation (RAG) pipeline.

---

## 🚀 Features
- **Benchmark Real-World Data:** Built on the Z24 Bridge Benchmark dataset loaded directly via Hugging Face (`thanglexuan/Z24-dataset-processed`).
- **Digital Signal Processing:** 4th-order Butterworth filtering (30 Hz cutoff), DC detrending, and channel standardization.
- **Physics-Informed Features:** Time-domain metrics (RMS, peak-to-peak, kurtosis) and FFT frequency-domain metrics (dominant frequency, spectral entropy).
- **Unsupervised Anomaly Detection:** Trained on healthy bridge operational baselines; evaluated on progressive structural damage scenarios.
- **Explainable AI (XAI):** SHAP values diagnose which exact vibration frequencies and sensor channels triggered an anomaly.
- **GenAI / RAG Incident Briefings:** ChromaDB vector database paired with MiniLM embeddings and Groq/Gemini LLMs to draft actionable inspection reports.
- **Interactive UI:** Streamlit multi-page dashboard featuring Plotly interactive waveforms and natural-language incident search.

---

## 📁 Repository Structure
```text
bridge-health/
├── context.md                # Full domain background, problem statement, and dataset specs
├── techstack.md              # Technical stack, library versions, and configuration
├── workflow.md               # Step-by-step engineering roadmap and execution plan
├── requirements.txt          # Pip dependencies
├── .gitignore                # Git ignore rules
│
├── data/
│   ├── download_z24.py       # Script to fetch/cache Z24 from Hugging Face
│   └── cache/                # Ignored cache directory
│
├── src/                      # Core modular Python packages
│   ├── __init__.py
│   ├── dataset_loader.py     # Z24 loader & scenario splitting
│   ├── preprocessing.py      # Detrending, Butterworth filtering, normalization
│   ├── features.py           # Time & FFT frequency feature extraction
│   ├── train.py              # Isolation Forest model training
│   ├── evaluate.py           # ROC-AUC and precision-recall evaluation
│   ├── explain.py            # SHAP attribution engine
│   ├── rag_indexer.py        # ChromaDB indexer for past incidents
│   └── report_generator.py   # RAG LLM incident advisory generator
│
├── models/                   # Trained model artifacts (.pkl)
│   └── .gitkeep
│
├── app/                      # Web dashboard
│   ├── __init__.py
│   └── dashboard.py          # Streamlit UI
│
├── notebooks/                # Exploratory Jupyter notebooks
│   ├── 01_explore_z24.ipynb
│   ├── 02_feature_analysis.ipynb
│   └── 03_anomaly_eval.ipynb
│
└── tests/                    # Automated unit tests
    ├── __init__.py
    ├── test_preprocessing.py
    ├── test_features.py
    └── test_model.py
```

---

## 🛠️ Quickstart

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-username/bridge-health.git
cd bridge-health

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Secrets
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run Pipeline & Dashboard
```bash
# Download and cache dataset
python data/download_z24.py

# Train anomaly detection model
python src/train.py

# Launch Streamlit dashboard
streamlit run app/dashboard.py
```

---

## 📚 References & Core Docs
- Detailed context and design: [`context.md`](context.md)
- Dependency and tech stack: [`techstack.md`](techstack.md)
- Step-by-step development guide: [`workflow.md`](workflow.md)
