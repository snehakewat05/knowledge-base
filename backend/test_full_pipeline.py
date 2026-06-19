import chromadb
from pathlib import Path
chroma_path = Path(__file__).parent.parent / "data" / "chroma"
client = chromadb.PersistentClient(path=str(chroma_path))
client.delete_collection("knowledge_base")
print("--- Cleared old ChromaDB data ---")

import sys
from pathlib import Path

# Make sure Python can find our modules
sys.path.append(str(Path(__file__).parent))

from ingestion.chunker import chunk_text
from ingestion.embedder import embed_chunks
from ingestion.store import store_chunks
from retrieval.retriever import retrieve_chunks
from llm.answerer import get_answer

# --- INGEST some sample knowledge ---
sample_text = """
Python is a high level programming language known for its simplicity and readability.
It is widely used in web development, data science, and artificial intelligence.
Django and FastAPI are popular Python web frameworks used to build APIs and web apps.
Pandas and NumPy are essential libraries for data analysis and numerical computing.
TensorFlow and PyTorch are the leading deep learning frameworks built on Python.
Guido van Rossum created Python in 1991. The name came from Monty Python.
Python uses indentation instead of curly braces to define code blocks.
Virtual environments in Python help isolate project dependencies cleanly.
""" * 3

print("--- Ingesting sample knowledge ---")
chunks = chunk_text(sample_text, chunk_size=50, overlap=20)
embedded = embed_chunks(chunks)
store_chunks(embedded, source_name="python_notes.txt")

# --- QUERY ---
question = "Who created Python and when?"

print(f"\n--- Question: {question} ---")

retrieved = retrieve_chunks(question, top_k=3)
print("\nTop chunks retrieved:")
for chunk in retrieved:
    print(f"\n  Score {chunk['relevance_score']} → {chunk['text']}")

print(f"\nTop {len(retrieved)} relevant chunks found:")
for chunk in retrieved:
    print(f"  [{chunk['source']}] score={chunk['relevance_score']} → {chunk['text'][:60]}...")

print("\n--- Ollama's Answer ---")
answer = get_answer(question, retrieved)
print(answer)