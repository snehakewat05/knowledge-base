import requests
from bs4 import BeautifulSoup
from pathlib import Path


def parse_url(url: str) -> dict:
    """
    Fetches a web article and extracts clean text from it.

    Args:
        url: Full URL of the article e.g. 'https://example.com/article'

    Returns:
        Dict with 'text', 'title', and 'source'
    """

    headers = {
        # Pretend to be a browser — some sites block plain Python requests
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # throws error if page not found

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title = soup.title.string.strip() if soup.title else "Unknown Title"

    # Remove junk elements we don't want
    for tag in soup(["script", "style", "nav", "footer",
                     "header", "aside", "form", "button"]):
        tag.decompose()

    # Extract all remaining paragraph text
    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text(separator=" ").strip() for p in paragraphs)
    text = " ".join(text.split())  # clean up extra whitespace

    if not text:
        raise ValueError(f"No readable text found at {url}")

    print(f"Extracted {len(text.split())} words from '{title}'")

    return {
        "text": text,
        "title": title,
        "source": url
    }