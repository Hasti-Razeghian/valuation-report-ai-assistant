import os

def generate_with_openai(prompt: str, model: str | None = None) -> str:
    """Optional LLM generation. Requires OPENAI_API_KEY."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY to use --generate.")

    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "Follow the user's evidence-grounding instructions exactly."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content or ""
