import fitz  # PyMuPDF
from pathlib import Path


def parse_pdf(filepath: str | Path) -> list[dict]:
    """
    Extracts text from a PDF file, page by page.

    Args:
        filepath: Path to the PDF file

    Returns:
        List of dicts with 'text', 'page_number', and 'source'
    """
    filepath = Path(filepath)
    doc = fitz.open(str(filepath))
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()

        # Skip empty pages
        if not text:
            continue

        pages.append({
            "text": text,
            "page_number": page_num + 1,  # human readable — starts at 1
            "source": filepath.name
        })

    doc.close()
    print(f"Extracted {len(pages)} pages from '{filepath.name}'")
    return pages