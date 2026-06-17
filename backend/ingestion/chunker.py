def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """
    Splits a long text into overlapping chunks.

    Args:
        text: The full document text
        chunk_size: How many words per chunk
        overlap: How many words to repeat between chunks

    Returns:
        A list of dicts, each with 'text' and 'chunk_index'
    """

    words = text.split()
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words)

        chunks.append({
            "text": chunk_text_str,
            "chunk_index": chunk_index
        })

        chunk_index += 1
        start += chunk_size - overlap  # step forward, but overlap a little

    return chunks