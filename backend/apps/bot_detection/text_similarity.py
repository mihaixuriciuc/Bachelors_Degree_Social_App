
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextSimilarityService:

    @staticmethod
    def pairwise_similarity(texts: list[str]):
        if len(texts) < 2:
            return None

        # Filter out completely empty strings — TfidfVectorizer errors on
        # an all-empty vocabulary.
        non_empty = [t for t in texts if t and t.strip()]
        if len(non_empty) < 2:
            return None

        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(non_empty)
        except ValueError:
            return None

        return cosine_similarity(tfidf_matrix)

    @staticmethod
    def max_pairwise_similarity(texts: list[str]) -> float:
        matrix = TextSimilarityService.pairwise_similarity(texts)
        if matrix is None:
            return 0.0

        n = matrix.shape[0]
        max_sim = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] > max_sim:
                    max_sim = matrix[i][j]
        return max_sim

    @staticmethod
    def count_similar_pairs(texts: list[str], threshold: float) -> int:
        matrix = TextSimilarityService.pairwise_similarity(texts)
        if matrix is None:
            return 0

        n = matrix.shape[0]
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] >= threshold:
                    count += 1
        return count

    @staticmethod
    def has_similar_cluster(texts: list[str], threshold: float) -> bool:

        return TextSimilarityService.count_similar_pairs(texts, threshold) >= 1