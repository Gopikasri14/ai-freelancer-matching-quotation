from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "sample" / "quotation_training.csv"
ARTIFACTS = ROOT / "backend" / "models"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "project_type", "complexity", "expected_hours", "experience_years",
    "deadline_days", "revisions", "budget", "hourly_rate", "minimum_rate"
]

def main():
    df = pd.read_csv(DATA)
    X = df[FEATURES]
    y_effort = df["actual_effort_hours"]
    y_price = df["actual_project_price"]

    categorical = ["project_type", "complexity"]
    numeric = [c for c in FEATURES if c not in categorical]
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric)
    ])

    effort_model = Pipeline([
        ("preprocessor", preprocessor),
        ("model", XGBRegressor(
            n_estimators=250, max_depth=4, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9, objective="reg:squarederror",
            random_state=42
        ))
    ])
    price_model = Pipeline([
        ("preprocessor", preprocessor),
        ("model", XGBRegressor(
            n_estimators=250, max_depth=4, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9, objective="reg:squarederror",
            random_state=42
        ))
    ])

    X_train, X_test, ye_train, ye_test, yp_train, yp_test = train_test_split(
        X, y_effort, y_price, test_size=0.2, random_state=42
    )
    effort_model.fit(X_train, ye_train)
    price_model.fit(X_train, yp_train)

    ep = effort_model.predict(X_test)
    pp = price_model.predict(X_test)

    print("EFFORT MAE:", round(mean_absolute_error(ye_test, ep), 3))
    print("EFFORT RMSE:", round(mean_squared_error(ye_test, ep) ** 0.5, 3))
    print("EFFORT R2:", round(r2_score(ye_test, ep), 3))
    print("PRICE MAE:", round(mean_absolute_error(yp_test, pp), 2))
    print("PRICE RMSE:", round(mean_squared_error(yp_test, pp) ** 0.5, 2))
    print("PRICE R2:", round(r2_score(yp_test, pp), 3))

    joblib.dump(effort_model, ARTIFACTS / "effort_model.joblib")
    joblib.dump(price_model, ARTIFACTS / "price_model.joblib")
    print("Saved models to", ARTIFACTS)

if __name__ == "__main__":
    main()
