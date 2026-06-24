import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from various YouTube URL formats.
    """
    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video ID from URL: {url}")


def parse_youtube(url: str) -> dict:
    """
    Fetches the transcript of a YouTube video.

    Args:
        url: YouTube video URL

    Returns:
        Dict with 'text', 'video_id', and 'source'
    """
    video_id = extract_video_id(url)
    print(f"Fetching transcript for video ID: {video_id}")

    # New API syntax for recent versions
    ytt_api = YouTubeTranscriptApi()
    fetched = ytt_api.fetch(video_id)

    # fetched is a FetchedTranscript object — iterate to get text
    full_text = " ".join(entry.text for entry in fetched)
    full_text = " ".join(full_text.split())  # clean whitespace

    word_count = len(full_text.split())
    print(f"Extracted {word_count} words from transcript")

    return {
        "text": full_text,
        "video_id": video_id,
        "source": f"youtube_{video_id}"
    }