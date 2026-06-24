from pathlib import Path
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_chunks
from ingestion.store import store_chunks
from ingestion.parsers.pdf_parser import parse_pdf
from ingestion.parsers.web_parser import parse_url
from ingestion.parsers.youtube_parser import parse_youtube


def is_youtube_url(text: str) -> bool:
    return "youtube.com/watch" in text or "youtu.be/" in text


def is_web_url(text: str) -> bool:
    return text.startswith("http://") or text.startswith("https://")


def ingest(source: str, raw_data_path: Path = None):
    """
    Universal ingestor — detects source type and routes accordingly.

    Args:
        source: A file name, URL, or YouTube link
        raw_data_path: Base path where local files are stored
    """

    # --- YouTube ---
    if is_youtube_url(source):
        print(f"\nDetected: YouTube video")
        result = parse_youtube(source)
        chunks = chunk_text(result["text"], chunk_size=60, overlap=20)
        source_name = result["source"]

    # --- Web URL ---
    elif is_web_url(source):
        print(f"\nDetected: Web article")
        result = parse_url(source)
        chunks = chunk_text(result["text"], chunk_size=60, overlap=20)
        source_name = result["title"][:50]

    # --- Local file ---
    else:
        if raw_data_path is None:
            raise ValueError("raw_data_path required for local files")

        filepath = raw_data_path / source

        if not filepath.exists():
            print(f"File not found: {filepath}")
            return

        # PDF
        if filepath.suffix.lower() == ".pdf":
            print(f"\nDetected: PDF file")
            pages = parse_pdf(filepath)
            chunks = []
            chunk_counter = 0
            for page in pages:
                page_chunks = chunk_text(
                    page["text"],
                    chunk_size=60,
                    overlap=20,
                    metadata={"page_number": page["page_number"]}
                )
                for chunk in page_chunks:
                    chunk["chunk_index"] = chunk_counter
                    chunk_counter += 1
                chunks.extend(page_chunks)
            source_name = filepath.name

        # Plain text or Markdown
        elif filepath.suffix.lower() in (".txt", ".md"):
            print(f"\nDetected: Text file")
            text = filepath.read_text(encoding="utf-8")
            chunks = chunk_text(text, chunk_size=60, overlap=20)
            source_name = filepath.name

        else:
            print(f"Unsupported file type: {filepath.suffix}")
            return

    # Embed and store
    embedded = embed_chunks(chunks)
    store_chunks(embedded, source_name=source_name)
    print(f"✅ Ingested '{source_name}' — {len(chunks)} chunks stored")