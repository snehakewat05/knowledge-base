import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import chromadb

from ingestion.ingestor import ingest
from ingestion.store import get_or_create_collection
from retrieval.retriever import retrieve_chunks
from llm.answerer import get_answer

app = FastAPI(title="Personal Knowledge Base API")

# Allow React frontend to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server port
    allow_methods=["*"],
    allow_headers=["*"],
)

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"
CHROMA_PATH = Path(__file__).parent.parent / "data" / "chroma"


# ── Request/Response Models ──────────────────────────────

class ChatRequest(BaseModel):
    question: str
    top_k: int = 3
    conversation_history: list[dict] = []


class SourceCard(BaseModel):
    source: str
    relevance_score: float
    text: str
    page_number: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceCard]


class IngestURLRequest(BaseModel):
    url: str


# ── Endpoints ────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "Personal Knowledge Base API is running"}


@app.get("/status")
def status():
    """Returns how many chunks are currently stored."""
    collection = get_or_create_collection()
    return {
        "chunks_stored": collection.count(),
        "status": "ready" if collection.count() > 0 else "empty"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Takes a question + conversation history,
    retrieves relevant chunks, and returns a grounded answer.
    """
    collection = get_or_create_collection()
    if collection.count() == 0:
        raise HTTPException(
            status_code=400,
            detail="Knowledge base is empty. Ingest some content first."
        )

    retrieved = retrieve_chunks(request.question, top_k=request.top_k)
    if not retrieved:
        raise HTTPException(status_code=404, detail="No relevant chunks found.")

    answer = get_answer(
        request.question,
        retrieved,
        conversation_history=request.conversation_history
    )

    sources = [
        SourceCard(
            source=chunk["source"],
            relevance_score=chunk["relevance_score"],
            text=chunk["text"],
            page_number=chunk.get("page_number")
        )
        for chunk in retrieved
    ]

    return ChatResponse(answer=answer, sources=sources)


@app.post("/ingest/url")
def ingest_url(request: IngestURLRequest):
    """Ingests a web article or YouTube video from a URL."""
    try:
        ingest(request.url, raw_data_path=RAW_DATA_PATH)
        collection = get_or_create_collection()
        return {
            "status": "success",
            "chunks_stored": collection.count()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest/file")
def ingest_file(file: UploadFile = File(...)):
    """
    Accepts a file upload (.txt, .pdf, .md)
    and ingests it into the knowledge base.
    """
    allowed = {".txt", ".pdf", ".md"}
    suffix = Path(file.filename).suffix.lower()

    if suffix not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}. Allowed: {allowed}"
        )

    # Save uploaded file to data/raw/
    save_path = RAW_DATA_PATH / file.filename
    with save_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        ingest(file.filename, raw_data_path=RAW_DATA_PATH)
        collection = get_or_create_collection()
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_stored": collection.count()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/sources")
def list_sources():
    """Returns all unique sources with their tags."""
    collection = get_or_create_collection()

    if collection.count() == 0:
        return {"sources": []}

    results = collection.get(include=["metadatas"])

    seen = {}
    for metadata in results["metadatas"]:
        source = metadata["source"]
        if source not in seen:
            tags = metadata.get("tags", "")
            seen[source] = {
                "name": source,
                "chunk_count": 1,
                "tags": tags.split(",") if tags else []
            }
        else:
            seen[source]["chunk_count"] += 1

    return {"sources": list(seen.values())}

@app.delete("/reset")
def reset():
    """Clears all data from the knowledge base."""
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    client.delete_collection("knowledge_base")
    return {"status": "Knowledge base cleared"}
@app.get("/sources")
def list_sources():
    """Returns all unique sources currently stored in ChromaDB."""
    collection = get_or_create_collection()

    if collection.count() == 0:
        return {"sources": []}

    # Get all stored items
    results = collection.get(include=["metadatas"])

    # Extract unique sources with their metadata
    seen = {}
    for metadata in results["metadatas"]:
        source = metadata["source"]
        if source not in seen:
            seen[source] = {
                "name": source,
                "chunk_count": 1
            }
        else:
            seen[source]["chunk_count"] += 1

    return {"sources": list(seen.values())}


@app.delete("/sources/{source_name:path}")
def delete_source(source_name: str):
    """Deletes all chunks belonging to a specific source."""
    collection = get_or_create_collection()

    # Find all IDs belonging to this source
    results = collection.get(include=["metadatas"])

    ids_to_delete = [
        results["ids"][i]
        for i, metadata in enumerate(results["metadatas"])
        if metadata["source"] == source_name
    ]

    if not ids_to_delete:
        raise HTTPException(
            status_code=404,
            detail=f"Source '{source_name}' not found"
        )

    collection.delete(ids=ids_to_delete)

    return {
        "status": "deleted",
        "source": source_name,
        "chunks_removed": len(ids_to_delete)
    }