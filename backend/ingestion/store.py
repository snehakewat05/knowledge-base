import chromadb
from pathlib import Path
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


def store_chunks(embedded_chunks: list[dict], source_name: str,
                 tags: list[str] = None):
    """
    Stores embedded chunks into ChromaDB.
    Optionally stores tags in each chunk's metadata.
    """
    collection = get_or_create_collection()

    ids        = []
    embeddings = []
    documents  = []
    metadatas  = []

    # Convert tags list to a string for ChromaDB
    # (ChromaDB metadata only supports strings, ints, floats, bools)
    tags_str = ",".join(tags) if tags else ""

    for chunk in embedded_chunks:
        chunk_id = f"{source_name}_chunk_{chunk['chunk_index']}"

        metadata = {
            "source": source_name,
            "chunk_index": chunk['chunk_index'],
            "tags": tags_str
        }
        if "page_number" in chunk:
            metadata["page_number"] = chunk["page_number"]

        ids.append(chunk_id)
        embeddings.append(chunk['embedding'])
        documents.append(chunk['text'])
        metadatas.append(metadata)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Stored {len(embedded_chunks)} chunks from '{source_name}'")