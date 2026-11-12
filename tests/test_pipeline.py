import unittest

from src.chunking import chunk_text, chunk_documents
from src.retrieval import TfidfRetriever
from src.prompting import build_prompt

class PipelineTests(unittest.TestCase):
    def test_chunking_preserves_source(self):
        chunks = chunk_text("one two three four five six", "doc-a", chunk_size=4, overlap=1)
        self.assertTrue(chunks)
        self.assertTrue(all(item["source_id"] == "doc-a" for item in chunks))

    def test_retrieval_finds_accessibility_passage(self):
        docs = [
            {"id": "access", "text": "A bus stop is 150 metres away. Eight parking spaces are behind the building."},
            {"id": "energy", "text": "The building has no energy label in the available documents."},
        ]
        chunks = chunk_documents(docs, chunk_size=100, overlap=0)
        results = TfidfRetriever(chunks).search("bus stop and parking", top_k=1)
        self.assertEqual(results[0]["source_id"], "access")

    def test_prompt_contains_evidence_and_guardrails(self):
        prompt = build_prompt("Describe access", [{
            "source_id": "access", "chunk_id": "access-1", "text": "A bus stop is nearby."
        }])
        self.assertIn("A bus stop is nearby.", prompt)
        self.assertIn("Use only the evidence", prompt)

if __name__ == "__main__":
    unittest.main()
