import chromadb
from pathlib import Path

CHROMA_PATH = Path(__file__).parent.parent.parent / "data" / "chroma"
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

client.delete_collection("knowledge_base")
print("✅ ChromaDB cleared successfully!")