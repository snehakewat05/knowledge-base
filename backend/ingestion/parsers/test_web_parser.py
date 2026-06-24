import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from ingestion.parsers.web_parser import parse_url
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_chunks
from ingestion.store import store_chunks

# Paste any article URL here
URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"

# Parse
article = parse_url(URL)
print(f"\nTitle: {article['title']}")
print(f"First 200 chars: {article['text'][:200]}")

# Chunk
chunks = chunk_text(article["text"], chunk_size=60, overlap=20)
print(f"\nTotal chunks: {len(chunks)}")

# Embed and store
embedded = embed_chunks(chunks)

# Use title as source name so citations are readable
source_name = article["title"][:50]  # trim if too long
store_chunks(embedded, source_name=source_name)

print(f"\n✅ Article ingested successfully as '{source_name}'")