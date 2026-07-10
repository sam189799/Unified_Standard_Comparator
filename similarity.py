from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load AI model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(text1, text2):
    """
    Calculate semantic similarity between two texts.
    """

    embeddings = model.encode([text1, text2])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(similarity * 100, 2)


def compare_clauses(clauses1, clauses2):
    """
    Compare clause-by-clause.
    """

    results = []

    all_clauses = sorted(
        set(clauses1.keys()) | set(clauses2.keys())
    )

    for clause in all_clauses:

        text1 = clauses1.get(clause, "")
        text2 = clauses2.get(clause, "")

        if text1 and text2:
            similarity = calculate_similarity(text1, text2)
        else:
            similarity = 0

        results.append({
            "clause": clause,
            "text1": text1,
            "text2": text2,
            "similarity": similarity
        })

    return results