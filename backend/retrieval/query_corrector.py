from rapidfuzz import process, fuzz
import chromadb
from pathlib import Path

CHROMA_PATH = Path(__file__).parent.parent.parent / "data" / "chroma"


def build_vocabulary() -> list[str]:
    """
    Pulls all stored text from ChromaDB and builds
    a vocabulary of unique meaningful words.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    try:
        collection = client.get_collection("knowledge_base")
    except Exception:
        return []

    if collection.count() == 0:
        return []

    results = collection.get(include=["documents"])
    all_text = " ".join(results["documents"])

    # Extract unique words longer than 4 chars
    words = set()
    for word in all_text.split():
        cleaned = word.strip(".,!?;:\"'()[]{}").lower()
        if len(cleaned) > 4:
            words.add(cleaned)

    return list(words)


def correct_query(query: str) -> str:
    """
    Checks each word in the query against the knowledge base
    vocabulary and corrects likely typos.

    Args:
        query: The raw user query

    Returns:
        Corrected query string
    """
    vocabulary = build_vocabulary()

    if not vocabulary:
        return query  # nothing to correct against

    corrected_words = []

    for word in query.split():
        cleaned = word.strip(".,!?;:\"'()[]{}").lower()

        # Only attempt correction for longer words
        if len(cleaned) <= 4:
            corrected_words.append(word)
            continue

        # Find the closest match in vocabulary
        match = process.extractOne(
            cleaned,
            vocabulary,
            scorer=fuzz.ratio,
            score_cutoff=75  # minimum similarity threshold
        )

        if match and match[0] != cleaned:
            print(f"Query correction: '{cleaned}' -> '{match[0]}'")
            corrected_words.append(match[0])
        else:
            corrected_words.append(word)

    return " ".join(corrected_words)