import sys
from pathlib import Path

# Make sure Python can find our modules
sys.path.append(str(Path(__file__).parent))

from ingestion.chunker import chunk_text
from ingestion.embedder import embed_chunks
from ingestion.store import store_chunks, get_or_create_collection
from retrieval.retriever import retrieve_chunks
from llm.answerer import get_answer

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"


def ingest_file(filepath: Path):
    """Reads a .txt file and runs it through the full ingestion pipeline."""
    print(f"\nIngesting: {filepath.name}...")

    text = filepath.read_text(encoding="utf-8")
    chunks = chunk_text(text, chunk_size=60, overlap=20)
    embedded = embed_chunks(chunks)
    store_chunks(embedded, source_name=filepath.name)

    print(f"✅ Done — {len(chunks)} chunks stored from '{filepath.name}'")


def ingest_all_files():
    """Ingests all .txt files found in data/raw/"""
    txt_files = list(RAW_DATA_PATH.glob("*.txt"))

    if not txt_files:
        print(f"\nNo .txt files found in {RAW_DATA_PATH}")
        print("Add some .txt files there and restart.\n")
        return

    print(f"\nFound {len(txt_files)} file(s) to ingest:")
    for f in txt_files:
        print(f"  - {f.name}")

    for f in txt_files:
        ingest_file(f)


def chat_loop():
    """Main interactive chat loop."""
    print("\n" + "="*50)
    print("   Personal Knowledge Base — CLI Chat")
    print("="*50)
    print("Type your question and press Enter.")
    print("Type 'quit' to exit.\n")

    # Check if anything is stored
    collection = get_or_create_collection()
    ingest_all_files()

    print(f"\nKnowledge base ready — {collection.count()} chunks loaded.")
    print("-"*50)

    while True:
        # Get user question
        question = input("\nYou: ").strip()

        if not question:
            continue

        if question.lower() in ("quit", "exit", "q"):
            print("\nGoodbye! 👋")
            break

        # Retrieve and answer
        print("\nSearching knowledge base...")
        retrieved = retrieve_chunks(question, top_k=3)

        if not retrieved:
            print("No relevant chunks found.")
            continue

        print(f"Found {len(retrieved)} relevant chunks — asking Llama...\n")
        answer = get_answer(question, retrieved)

        print(f"Assistant: {answer}")
        print("\nSources used:")
        for chunk in retrieved:
            print(f"  [{chunk['source']}] score={chunk['relevance_score']}")


if __name__ == "__main__":
    chat_loop()