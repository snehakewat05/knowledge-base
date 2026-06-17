from chunker import chunk_text
from embedder import embed_chunks
from store import store_chunks, get_or_create_collection

sample_text = """
Python is a high level programming language known for its simplicity.
It is widely used in web development, data science, and artificial intelligence.
Django and FastAPI are popular Python web frameworks.
Pandas and NumPy are essential libraries for data analysis in Python.
TensorFlow and PyTorch are the leading deep learning frameworks built on Python.
""" * 5

# Full pipeline: chunk → embed → store
chunks = chunk_text(sample_text, chunk_size=50, overlap=10)
embedded = embed_chunks(chunks)
store_chunks(embedded, source_name="python_notes.txt")

# Verify it was actually stored
collection = get_or_create_collection()
print(f"\nTotal chunks in ChromaDB: {collection.count()}")

# Peek at what's stored
result = collection.get(limit=2, include=["documents", "metadatas"])
print(f"\nSample stored chunk:")
print(f"Text: {result['documents'][0][:80]}...")
print(f"Metadata: {result['metadatas'][0]}")