from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfRetriever:
    """Lightweight retriever for the synthetic demo corpus."""

    def __init__(self, chunks: list[dict]):
        if not chunks:
            raise ValueError("At least one chunk is required.")
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([chunk["text"] for chunk in chunks])

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        ranked = scores.argsort()[::-1][:top_k]

        results = []
        for index in ranked:
            if scores[index] <= 0:
                continue
            result = dict(self.chunks[index])
            result["score"] = float(scores[index])
            results.append(result)
        return results
