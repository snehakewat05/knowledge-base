from chunker import chunk_text
from embedder import embed_chunks

sample_text = """
Artificial intelligence is transforming the world. Machine learning allows 
computers to learn from data. Deep learning uses neural networks with many 
layers. Natural language processing helps machines understand human text.
""" * 5

# Step 1: chunk
chunks = chunk_text(sample_text, chunk_size=50, overlap=10)
print(f"Chunks created: {len(chunks)}")

# Step 2: embed
embedded_chunks = embed_chunks(chunks)

# Inspect the first chunk
first = embedded_chunks[0]
print(f"\nChunk 0 text: {first['text'][:80]}...")
print(f"Embedding length: {len(first['embedding'])}")
print(f"First 5 numbers: {first['embedding'][:5]}")