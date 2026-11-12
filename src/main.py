import argparse
import json
from pathlib import Path

from src.chunking import chunk_documents
from src.retrieval import TfidfRetriever
from src.prompting import build_prompt
from src.generation import generate_with_openai

ROOT = Path(__file__).resolve().parents[1]

def load_documents() -> list[dict]:
    with (ROOT / "data" / "sample_documents.json").open(encoding="utf-8") as file:
        return json.load(file)

def run(question: str, generate: bool = False) -> None:
    documents = load_documents()
    chunks = chunk_documents(documents)
    retriever = TfidfRetriever(chunks)
    results = retriever.search(question, top_k=4)

    print("\n=== Retrieved evidence ===")
    if not results:
        print("No relevant source passages were found.")
    for item in results:
        print(f"\n[{item['source_id']} | {item['chunk_id']} | score={item['score']:.3f}]")
        print(item["text"])

    prompt = build_prompt(question, results)
    print("\n=== Grounded prompt ===")
    print(prompt)

    if generate:
        print("\n=== Draft for human review ===")
        print(generate_with_openai(prompt))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the valuation report RAG demo.")
    parser.add_argument("--question", required=True, help="Factual question to answer.")
    parser.add_argument("--generate", action="store_true", help="Call the optional OpenAI generation step.")
    args = parser.parse_args()
    run(args.question, args.generate)
