# Tech Stack & Dependency Specification

## 1. Environment & Architecture
- **Architecture Pattern:** Decoupled Full-Stack Web Application (SPA + REST API)
- **Backend Runtime:** Python 3.11 with FastAPI & Uvicorn
- **Frontend Runtime:** Node.js with React (Vite) & Tailwind CSS
- **Environment Management:** Conda / uv (`requirements.txt`) & npm (`package.json`)
- **Version Control:** Git & GitHub

---

## 2. Core Libraries & Responsibilities

### Backend (Python 3.11)
| Category | Library / Tool | Purpose & Usage Details |
|---|---|---|
| **Web Framework & API** | `fastapi`, `uvicorn` | High-performance asynchronous REST API serving frontend requests |
| **Data Ingestion** | `datasets` (Hugging Face) | Programmatically pull `thanglexuan/Z24-dataset-processed` from HF hub |
| **Numeric & Signal Processing** | `numpy` | Multi-dimensional array slicing on `(1530, 27, 6000)` tensors |
| | `scipy` (`scipy.signal`, `scipy.fft`) | Detrending, 4th-order Butterworth filter, FFT dominant frequency, spectral entropy |
| | `pandas` | Structured tabular feature management, metadata handling, CSV export |
| **Machine Learning & Time-Series** | `scikit-learn` | `IsolationForest`, `StandardScaler`, `roc_auc_score`, `precision_recall_curve` |
| | `statsmodels` | `ARIMA` / `SARIMAX` for structural degradation forecasting and trend analysis |
| | `joblib` | Model persistence (`isolation_forest.pkl`, `scaler.pkl`) |
| **Explainable AI (XAI)** | `shap` | `TreeExplainer` for per-feature SHAP value calculations and diagnostic attribution |
| **Embeddings & Vector Store** | `sentence-transformers` | `all-MiniLM-L6-v2` dense 384-dimensional text embeddings |
| | `chromadb` | Local vector database storing incident vectors and similarity querying |
| **LLM Orchestration & GenAI**| `langchain` / `langchain-community` | Document loaders, prompt templates, RAG chains |
| | `langchain-groq` | Fast inference via Llama 3.3 models on Groq cloud |
| | `langchain-google-genai` | Fallback / alternative LLM inference via Gemini Flash |
| **Testing & Quality** | `pytest` | Unit testing data transformations, feature shapes, and API endpoints |

### Frontend (React + Tailwind)
| Category | Tool / Package | Purpose |
|---|---|---|
| **Framework & Build** | React 18, Vite | Lightning-fast development server and optimized production build |
| **Styling** | Tailwind CSS | Modern utility-first responsive styling |
| **Iconography** | `lucide-react` | Clean, modern UI icons for alerts, status indicators, and controls |
| **Data Visualization** | `recharts` / `chart.js` | Interactive waveform line charts, FFT spectra, ARIMA forecast curves, and SHAP bar charts |
| **HTTP Client** | `axios` or native `fetch` | Communicating with FastAPI backend endpoints |

---

## 3. Recommended Backend `requirements.txt`
```text
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
datasets>=2.19.0
numpy>=1.26.0
scipy>=1.13.0
pandas>=2.2.0
scikit-learn>=1.4.0
statsmodels>=0.14.0
joblib>=1.3.0
shap>=0.45.0
sentence-transformers>=2.7.0
chromadb>=0.5.0
langchain>=0.2.0
langchain-community>=0.2.0
langchain-groq>=0.1.0
langchain-google-genai>=1.0.0
pytest>=8.2.0
python-dotenv>=1.0.1
```

---

## 4. Key Configuration Variables & API Keys
Store these in `.env` (never commit to git):
- `GROQ_API_KEY`: Groq Cloud API Key for rapid LLM report generation.
- `GEMINI_API_KEY`: Google Gemini API Key as alternate LLM provider.
- `HF_TOKEN`: (Optional) Hugging Face read access token.
