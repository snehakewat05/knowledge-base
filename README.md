# Personal Knowledge Base
### AI-Powered Second Brain

A self-hosted, fully local knowledge base that lets you ingest any content — notes, PDFs, articles, YouTube videos — and have a natural conversation with all of it.

---

## Features

- Conversational search over all your documents
- Supports PDF, plain text, web articles and YouTube videos
- Auto-tagging of every ingested source
- Typo-tolerant fuzzy search
- Conversation memory with auto-summarization
- Browser extension to clip articles in one click
- Full source attribution with relevance scores
- 100% local — no data leaves your machine except Claude API calls

---

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI |
| LLM | Ollama (llama3.2) |
| Embeddings | sentence-transformers |
| Vector DB | ChromaDB |
| PDF Parsing | PyMuPDF |
| Web Scraping | BeautifulSoup |
| YouTube | youtube-transcript-api |

---

## Project Structure

```
knowledge-base/
├── backend/
│   ├── ingestion/
│   │   ├── parsers/
│   │   │   ├── pdf_parser.py
│   │   │   ├── web_parser.py
│   │   │   └── youtube_parser.py
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   ├── ingestor.py
│   │   ├── store.py
│   │   └── tagger.py
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── query_corrector.py
│   ├── llm/
│   │   ├── answerer.py
│   │   └── summarizer.py
│   ├── cli.py
│   └── main.py
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── ChatMessage.jsx
│       │   ├── IngestBar.jsx
│       │   └── Sidebar.jsx
│       └── App.jsx
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
├── data/
│   ├── raw/
│   └── chroma/
├── .env
├── requirements.txt
└── README.md
```

---

## Setup Guide

### Prerequisites
- Python 3.10+
- Node.js 18+
- Ollama installed from [ollama.com](https://ollama.com)

### 1 — Clone the repo
```bash
git clone https://github.com/yourusername/personal-knowledge-base.git
cd personal-knowledge-base
```

### 2 — Set up Python environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 3 — Set up environment variables
Create a `.env` file in the root:
```
ANTHROPIC_API_KEY=your_key_here   # optional
```

### 4 — Pull the Ollama model
```bash
ollama pull llama3.2
```

### 5 — Run the backend
```bash
cd backend
uvicorn main:app --reload
```

### 6 — Run the frontend
```bash
cd frontend
npm install
npm run dev
```

### 7 — Open the app
Visit `http://localhost:5173` in your browser.

### 8 — Install the browser extension
1. Go to `chrome://extensions/`
2. Enable Developer Mode
3. Click Load Unpacked
4. Select the `extension/` folder

---

## Daily Usage

Every time you work on the project:

| Terminal | Command |
|---|---|
| Terminal 1 | `ollama serve` (if not auto-started) |
| Terminal 2 | `cd backend && uvicorn main:app --reload` |
| Terminal 3 | `cd frontend && npm run dev` |

---

## How It Works

```
Your Question
    ↓  fuzzy correction
    ↓  embed query
    ↓  search ChromaDB → top 3 chunks
    ↓  send chunks + conversation memory to Llama
    ↓  grounded, cited answer
```