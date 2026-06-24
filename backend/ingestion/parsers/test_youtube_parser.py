import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from ingestion.parsers.youtube_parser import parse_youtube
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_chunks
from ingestion.store import store_chunks

# Paste any YouTube video URL that has captions/subtitles
URL = "https://www.youtube.com/watch?v=aircAruvnKk"
# This is 3Blue1Brown's 'But what is a neural network?' — has great captions

# Parse
video = parse_youtube(URL)
print(f"\nVideo ID: {video['video_id']}")
print(f"First 200 chars: {video['text'][:200]}")

# Chunk
chunks = chunk_text(video["text"], chunk_size=60, overlap=20)
print(f"\nTotal chunks: {len(chunks)}")

# Embed and store
embedded = embed_chunks(chunks)
store_chunks(embedded, source_name=video["source"])

print(f"\n✅ YouTube video ingested as '{video['source']}'")