from sentence_transformers import SentenceTransformer

# Load the model once — reusing it is much faster than reloading every time
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes a list of chunk dicts and adds an 'embedding' key to each one.

    Args:
        chunks: List of dicts with 'text' and 'chunk_index'

    Returns:
        Same list but each dict now also has an 'embedding' key
    """

    # Extract just the text from each chunk for batch processing
    texts = [chunk['text'] for chunk in chunks]

    # Embed all texts in one batch — much faster than one by one
    embeddings = model.encode(texts, show_progress_bar=True)

    # Attach each embedding back to its chunk
    for i, chunk in enumerate(chunks):
        chunk['embedding'] = embeddings[i].tolist()  # convert numpy array to plain list

    return chunks