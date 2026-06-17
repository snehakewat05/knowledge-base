from chunker import chunk_text

sample_text = """
Artificial intelligence is transforming the world. Machine learning allows computers 
to learn from data. Deep learning uses neural networks with many layers. Natural 
language processing helps machines understand human text. These technologies are 
being applied across healthcare, finance, and education. The pace of progress is 
accelerating every year. Researchers are exploring new architectures and training 
methods. The future of AI remains both exciting and uncertain.
""" * 10  # repeat to make it long enough to chunk

chunks = chunk_text(sample_text, chunk_size=50, overlap=10)

print(f"Total chunks created: {len(chunks)}")
print()
for chunk in chunks[:3]:  # show first 3 chunks
    print(f"--- Chunk {chunk['chunk_index']} ---")
    print(chunk['text'])
    print()