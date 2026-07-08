import ollama


def summarize_conversation(messages: list[dict]) -> str:
    """
    Takes a list of conversation messages and returns
    a concise summary of what was discussed.

    Args:
        messages: List of dicts with 'role' and 'content'

    Returns:
        A short summary string
    """

    if not messages:
        return ""

    # Format conversation for Llama
    conversation_text = ""
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_text += f"{role}: {msg['content']}\n\n"

    prompt = f"""Summarize the following conversation in 3-4 sentences.
Focus on the key topics discussed and any important facts mentioned.
Be concise — this summary will be used as memory context.

Conversation:
{conversation_text}

Summary:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content'].strip()