import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from ingestion.ingestor import ingest
from ingestion.store import get_or_create_collection
from retrieval.retriever import retrieve_chunks
from llm.answerer import get_answer

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"


def print_banner():
    print("\n" + "="*55)
    print("      Personal Knowledge Base — CLI Chat")
    print("="*55)
    print("Commands:")
    print("  ingest: <filename or URL>  — add new content")
    print("  reset                      — clear all data")
    print("  quit                       — exit")
    print("  Or just type any question!")
    print("="*55 + "\n")


def chat_loop():
    print_banner()

    collection = get_or_create_collection()
    count = collection.count()

    if count == 0:
        print("Knowledge base is empty.")
        print(f"Add files to data/raw/ or type: ingest: <url>\n")
    else:
        print(f"Knowledge base ready — {count} chunks loaded.\n")

    print("-"*55)

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        # --- Quit ---
        if user_input.lower() in ("quit", "exit", "q"):
            print("\nGoodbye! 👋")
            break

        # --- Reset ---
        elif user_input.lower() == "reset":
            import chromadb
            client = chromadb.PersistentClient(
                path=str(Path(__file__).parent.parent / "data" / "chroma")
            )
            client.delete_collection("knowledge_base")
            print("✅ Knowledge base cleared!")

        # --- Ingest ---
        elif user_input.lower().startswith("ingest:"):
            source = user_input[7:].strip()  # everything after 'ingest:'
            if not source:
                print("Please provide a file name or URL after 'ingest:'")
            else:
                ingest(source, raw_data_path=RAW_DATA_PATH)

        # --- Question ---
        else:
            collection = get_or_create_collection()
            if collection.count() == 0:
                print("Knowledge base is empty — ingest something first!")
                continue

            print("\nSearching knowledge base...")
            retrieved = retrieve_chunks(user_input, top_k=3)

            if not retrieved:
                print("No relevant chunks found.")
                continue

            print(f"Found {len(retrieved)} chunks — thinking...\n")
            answer = get_answer(user_input, retrieved)

            print(f"Assistant: {answer}")
            print("\nSources:")
            for chunk in retrieved:
                source_info = f"  [{chunk['source']}] score={chunk['relevance_score']}"
                if "page_number" in chunk:
                    source_info += f" page={chunk['page_number']}"
                print(source_info)


if __name__ == "__main__":
    chat_loop()