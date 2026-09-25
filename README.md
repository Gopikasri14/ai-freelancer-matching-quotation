# AI-Powered Freelancer Matching and Quotation Optimization System

A production-style web application designed to connect clients with qualified freelancers using machine learning recommendation and generate transparent, explainable project quotations calibrated in Indian Rupees (₹ / INR).

---

## Architecture Overview
The application follows a **Modular Monolith** architecture:
* **Backend**: Python 3.11+, FastAPI, PostgreSQL, SQLAlchemy 2.0 (async), Alembic
* **Machine Learning**:
  * Semantic requirement matching: **TF-IDF + Cosine Similarity + Jaccard Skill Overlap**
  * Effort estimation: **XGBoost Regressor** (predicting hours)
  * Baseline quotation: **XGBoost Regressor** (predicting baseline cost in ₹)
  * Final price adjustment: **Deterministic Rule-Based Optimizer**
* **Frontend**: React 18, TypeScript, Tailwind CSS (Milestone 16+)

---

## Milestone 1: Development Environment Setup

### 1. Prerequisites
* **Python 3.11+**
* **Git for Windows**
* **Node.js 18+ LTS** (for subsequent frontend milestones)

### 2. Quickstart (Windows PowerShell)

```powershell
# 1. Create a virtual environment using Python 3.11
py -3.11 -m venv .venv

# 2. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Run the FastAPI development server
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Verify Health & API Documentation
* **Health Check**: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
* **Swagger Interactive Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
