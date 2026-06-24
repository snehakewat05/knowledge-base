def chunk_text(text: str, chunk_size: int = 60, overlap: int = 20,
               metadata: dict = None) -> list[dict]:
    """
    Splits text into overlapping chunks.
    Optionally carries extra metadata (e.g. page_number) into each chunk.
    """
    words = text.split()
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words)

        chunk = {
            "text": chunk_text_str,
            "chunk_index": chunk_index
        }

        # Carry any extra metadata (like page_number) into the chunk
        if metadata:
            chunk.update(metadata)

        chunks.append(chunk)
        chunk_index += 1
        start += chunk_size - overlap

    return chunks