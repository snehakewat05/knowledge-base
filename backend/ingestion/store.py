import chromadb
from pathlib import Path

# Point ChromaDB to our local data folder — this is where it saves everything
CHROMA_PATH = Path(__file__).parent.parent.parent / "data" / "chroma"

# Create a persistent client — data survives between runs
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

def get_or_create_collection(collection_name: str = "knowledge_base"):
    """
    Gets existing collection or creates a new one.
    A collection is like a table in a normal database.
    """
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # use cosine similarity for search
    )


def store_chunks(embedded_chunks: list[dict], source_name: str):
    """
    Stores embedded chunks into ChromaDB.

    Args:
        embedded_chunks: List of chunk dicts with 'text', 'chunk_index', 'embedding'
        source_name: Name of the source document e.g. 'my_notes.txt'
    """
    collection = get_or_create_collection()

    # ChromaDB needs three things for each chunk:
    ids         = []  # unique ID for each chunk
    embeddings  = []  # the vector
    documents   = []  # the raw text
    metadatas   = []  # extra info we want to store alongside

    for chunk in embedded_chunks:
        chunk_id = f"{source_name}_chunk_{chunk['chunk_index']}"

        ids.append(chunk_id)
        embeddings.append(chunk['embedding'])
        documents.append(chunk['text'])
        metadatas.append({
            "source": source_name,
            "chunk_index": chunk['chunk_index']
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Stored {len(embedded_chunks)} chunks from '{source_name}' into ChromaDB")