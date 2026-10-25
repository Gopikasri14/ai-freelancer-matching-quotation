# AI Freelancer Matching & Quotation Optimization System

A full-stack college/project MVP implementing:

Client requirements → TF-IDF + cosine similarity → freelancer recommendations → selected freelancer → XGBoost effort/price prediction → rule-based quotation optimization.

> Training data in `data/sample/` is synthetic and clearly labelled. It is for development/demo purposes and must not be presented as real market pricing.

## Stack
- Backend: FastAPI, SQLAlchemy, SQLite
- ML: scikit-learn TF-IDF/cosine similarity, XGBoost, pandas, joblib
- Frontend: React + Vite
- Database: SQLite for local development; can be replaced with PostgreSQL later

## Run backend
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.seed
python -m app.ml.train
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

## Run frontend
Open another terminal:
```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (normally http://localhost:5173).

## Core workflow
1. Enter project requirements.
2. Create the project.
3. Click Find Freelancers.
4. Review TF-IDF/cosine similarity scores.
5. Select a freelancer.
6. Generate a quotation.
7. View effort, base price, adjustments and recommended range.

## Important
The quotation model is trained from synthetic sample records generated for this prototype. Replace the sample data with permitted historical project data before making real pricing decisions.
