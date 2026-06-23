
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextSimilarityService:

    @staticmethod
    def pairwise_similarity(texts: list[str]):
        if len(texts) < 2:
            return None


        non_empty = [t for t in texts if t and t.strip()] # checks for empty strings
        if len(non_empty) < 2:
            return None

        try:
            vectorizer = TfidfVectorizer(stop_words='english') # ignores words of coonection
            tfidf_matrix = vectorizer.fit_transform(non_empty) # here tf -idf happens, for each text how frequent every word is and from all the texts in how many the word appears, logarithmic
        except ValueError:
            return None

        return cosine_similarity(tfidf_matrix) #makes everything to cosine between the vectors, so the magnitude does not matter, they just point to the same direction


    @staticmethod
    def count_similar_pairs(texts: list[str], threshold: float) -> int:  # counts the PAIRS found, 2 by 2
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
    def has_similar_cluster(texts: list[str], threshold: float) -> bool: # counts if there are more than 1

        return TextSimilarityService.count_similar_pairs(texts, threshold) >= 1