import ollama
from llm.summarizer import summarize_conversation

# How many recent messages to keep in full
# Older messages beyond this get summarized
RECENT_MESSAGES_LIMIT = 4


def get_answer(query: str, retrieved_chunks: list[dict],
               conversation_history: list[dict] = None) -> str:
    """
    Sends query + retrieved chunks + conversation memory to Llama.

    Args:
        query: Current user question
        retrieved_chunks: Relevant chunks from ChromaDB
        conversation_history: Full list of past messages

    Returns:
        Llama's answer as a string
    """

    # Build context from retrieved chunks
    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        context += f"\n[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n"

    # Build memory from conversation history
    memory = ""
    if conversation_history and len(conversation_history) > 0:

        if len(conversation_history) > RECENT_MESSAGES_LIMIT:
            # Summarize older messages
            older = conversation_history[:-RECENT_MESSAGES_LIMIT]
            recent = conversation_history[-RECENT_MESSAGES_LIMIT:]

            summary = summarize_conversation(older)
            memory += f"Earlier in our conversation:\n{summary}\n\n"

            # Add recent messages in full
            memory += "Recent exchanges:\n"
            for msg in recent:
                role = "User" if msg["role"] == "user" else "Assistant"
                memory += f"{role}: {msg['content']}\n"
        else:
            # All messages fit — no summarization needed
            memory += "Conversation so far:\n"
            for msg in conversation_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                memory += f"{role}: {msg['content']}\n"

    # Build the final prompt
    prompt = f"""You are a helpful assistant for a personal knowledge base.
Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I don't have information about that in your knowledge base."
Always mention which source your answer came from.

{f"CONVERSATION MEMORY:{memory}" if memory else ""}

KNOWLEDGE BASE CONTEXT:
{context}

CURRENT QUESTION: {query}

ANSWER:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']