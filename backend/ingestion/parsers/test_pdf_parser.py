import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from ingestion.parsers.pdf_parser import parse_pdf
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_chunks
from ingestion.store import store_chunks

# --- Point this to any PDF you have ---
PDF_PATH = Path(__file__).parent.parent.parent.parent / "data" / "raw" / "sample.pdf"

if not PDF_PATH.exists():
    print(f"Please add a PDF at: {PDF_PATH}")
    exit()

# Parse → chunk → embed → store
pages = parse_pdf(PDF_PATH)

all_chunks = []
chunk_counter = 0  # global counter across all pages

for page in pages:
    page_chunks = chunk_text(
        page["text"],
        chunk_size=60,
        overlap=20,
        metadata={"page_number": page["page_number"]}
    )
    # Give each chunk a globally unique index
    for chunk in page_chunks:
        chunk["chunk_index"] = chunk_counter
        chunk_counter += 1

    all_chunks.extend(page_chunks)

print(f"Total chunks from PDF: {len(all_chunks)}")

embedded = embed_chunks(all_chunks)
store_chunks(embedded, source_name="sample.pdf")
print("PDF ingested successfully!")