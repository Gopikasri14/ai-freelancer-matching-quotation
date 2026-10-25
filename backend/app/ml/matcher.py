from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def freelancer_text(freelancer):
    return " ".join([
        freelancer.name or "",
        freelancer.bio or "",
        freelancer.skills or ""
    ])

def match_freelancers(project, freelancers, top_k=5):
    if not freelancers:
        return []
    query = f"{project.title} {project.project_type} {project.description}"
    documents = [freelancer_text(f) for f in freelancers]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(documents + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    ranked = sorted(zip(freelancers, scores), key=lambda x: x[1], reverse=True)
    return [(f, float(score)) for f, score in ranked[:top_k]]
