import ollama


def generate_tags(text: str, max_tags: int = 5) -> list[str]:
    """
    Uses Llama to generate relevant tags for a piece of text.

    Args:
        text: Sample text from the ingested document
        max_tags: Maximum number of tags to generate

    Returns:
        List of tag strings e.g. ['fashion', 'history', 'magazine']
    """

    # Use first 500 words only — enough context, saves time
    sample = " ".join(text.split()[:500])

    prompt = f"""Read the following text and generate exactly {max_tags} single-word 
or two-word tags that best describe its topic and content.

Rules:
- Return ONLY the tags, one per line
- No numbers, no bullets, no explanations
- Lowercase only
- No hashtags

Text:
{sample}

Tags:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response['message']['content']

    # Parse response into clean list
    tags = []
    for line in raw.strip().split("\n"):
        tag = line.strip().lower()
        tag = tag.strip("•-–—*#")  # remove any stray symbols
        tag = tag.strip()
        if tag and len(tag) > 1:
            tags.append(tag)

    return tags[:max_tags]