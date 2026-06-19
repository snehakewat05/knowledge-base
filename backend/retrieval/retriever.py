from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path

CHROMA_PATH = Path(__file__).parent.parent.parent / "data" / "chroma"

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

def retrieve_chunks(query: str, top_k: int = 3) -> list[dict]:
    """
    Embeds the query and finds the most similar chunks in ChromaDB.

    Args:
        query: The user's question
        top_k: How many chunks to retrieve (3-5 is ideal)

    Returns:
        List of the most relevant chunks with text and metadata
    """

    # Embed the question using the same model we used for documents
    query_embedding = model.encode(query).tolist()

    collection = client.get_or_create_collection(
        name="knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )

    # Search ChromaDB for closest matching chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # Package results into clean dicts
    chunks = []
    for i in range(len(results['documents'][0])):
        chunks.append({
            "text": results['documents'][0][i],
            "source": results['metadatas'][0][i]['source'],
            "chunk_index": results['metadatas'][0][i]['chunk_index'],
            "relevance_score": round(1 - results['distances'][0][i], 3)
            # distance → similarity: closer to 1.0 = more relevant
        })

    return chunks