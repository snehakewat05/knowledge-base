import ollama

def get_answer(query: str, retrieved_chunks: list[dict]) -> str:
    """
    Sends the query + retrieved chunks to local Llama model via Ollama.
    Runs 100% locally — no API key, no cost, no data leaves your machine.
    """

    # Build context from retrieved chunks
    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        context += f"\n[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n"

    prompt = f"""You are a helpful assistant for a personal knowledge base.
Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I don't have information about that in your knowledge base."
Always mention which source your answer came from.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']