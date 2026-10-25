from pathlib import Path
import json
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = ROOT / "backend" / "models"

def predict(project, freelancer):
    effort_path = MODEL_DIR / "effort_model.joblib"
    price_path = MODEL_DIR / "price_model.joblib"
    if not effort_path.exists() or not price_path.exists():
        raise RuntimeError("Quotation models are not trained. Run: python -m app.ml.train")

    row = pd.DataFrame([{
        "project_type": project.project_type,
        "complexity": project.complexity,
        "expected_hours": project.expected_hours or 0,
        "experience_years": freelancer.experience_years,
        "deadline_days": project.deadline_days,
        "revisions": project.revisions,
        "budget": project.budget or 0,
        "hourly_rate": freelancer.hourly_rate,
        "minimum_rate": freelancer.minimum_rate
    }])

    effort = float(joblib.load(effort_path).predict(row)[0])
    base = float(joblib.load(price_path).predict(row)[0])

    complexity_factor = {"Low": 0.0, "Medium": 0.05, "High": 0.15}.get(project.complexity, 0.05)
    rush_factor = 0.20 if project.deadline_days <= 7 else 0.0
    revision_factor = max(0, project.revisions - 2) * 0.05

    adjusted = base * (1 + complexity_factor + rush_factor + revision_factor)
    minimum = max(adjusted * 0.92, freelancer.minimum_rate * max(effort, 1))
    maximum = adjusted * 1.08
    if project.budget:
        maximum = min(maximum, project.budget * 1.10)
        minimum = min(minimum, maximum)

    extra_revision = max(500.0, freelancer.hourly_rate * 2)
    return {
        "predicted_effort": round(effort, 1),
        "effort_min": round(max(1, effort * 0.9), 1),
        "effort_max": round(effort * 1.1, 1),
        "base_price": round(max(base, 0), 2),
        "final_min_price": round(max(minimum, 0), 2),
        "final_max_price": round(max(maximum, minimum), 2),
        "included_revisions": project.revisions,
        "extra_revision_price": round(extra_revision, 2),
        "adjustments": {
            "complexity_percent": round(complexity_factor * 100, 1),
            "rush_percent": round(rush_factor * 100, 1),
            "extra_revision_percent": round(revision_factor * 100, 1)
        }
    }
