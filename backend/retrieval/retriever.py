from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
from retrieval.query_corrector import correct_query

CHROMA_PATH = Path(__file__).parent.parent.parent / "data" / "chroma"

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

def retrieve_chunks(query: str, top_k: int = 3) -> list[dict]:
    """
    Corrects the query for typos then retrieves
    the most semantically similar chunks from ChromaDB.
    """

    # Step 1 — correct typos before embedding
    corrected = correct_query(query)
    if corrected != query:
        print(f"Original query: '{query}'")
        print(f"Corrected query: '{corrected}'")

    # Step 2 — embed the corrected query
    query_embedding = model.encode(corrected).tolist()

    collection = client.get_or_create_collection(
        name="knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )

    # Step 3 — search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for i in range(len(results['documents'][0])):
        chunks.append({
            "text": results['documents'][0][i],
            "source": results['metadatas'][0][i]['source'],
            "chunk_index": results['metadatas'][0][i]['chunk_index'],
            "relevance_score": round(1 - results['distances'][0][i], 3)
        })

    return chunks