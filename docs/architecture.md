# Architecture

Client -> React frontend -> FastAPI -> services -> ML/database.

Matching:
project text -> TF-IDF -> cosine similarity -> ranked freelancers.

Quotation:
project + freelancer features -> XGBoost effort/price models -> transparent rule-based optimizer -> quotation range.
