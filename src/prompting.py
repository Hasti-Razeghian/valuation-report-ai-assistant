def build_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    evidence = "\n\n".join(
        f"[Source: {chunk['source_id']} | Chunk: {chunk['chunk_id']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    return f"""You are helping draft a factual section of a property report.

Use only the evidence below. Do not use outside knowledge or infer facts that are
not explicitly supported. If the evidence does not answer part of the question,
state that the information is not available in the provided sources. Use clear,
neutral, professional language. Do not make a valuation, legal conclusion, or
recommendation.

QUESTION
{question}

SOURCE EVIDENCE
{evidence}

Write a concise factual draft. Do not hide uncertainty.
"""
