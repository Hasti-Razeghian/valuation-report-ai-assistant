# Valuation Report AI Assistant

A Python-based RAG system for drafting factual sections of property valuation reports using information retrieved from existing documents.

The system processes source documents, retrieves relevant information based on a user query, and uses an LLM to generate a draft based on the retrieved evidence. Each draft is returned with its supporting source passages for human review. A human remains responsible for reviewing the result.

> **Scope and provenance:** This is an independent demonstration built with synthetic example data. It is not Planon's production system and contains no Planon documents, source code, customer data, or confidential information. Retrieval can also be tested independently, without making an LLM API call.

## What it does

1. Loads synthetic property information from `data/sample_documents.json`.
2. Splits the source text into smaller chunks.
3. Converts document chunks into TF-IDF vectors and ranks them using cosine similarity.
4. Builds a grounded prompt from the retrieved evidence.
5. Sends that prompt to an LLM through the OpenAI API.
6. Returns the generated draft together with the source passages for human verification.

## Architecture

```text
Synthetic source documents
          |
          v
   Text chunking
          |
          v
  TF-IDF vectorization
          |
          v
 Semantic retrieval <----- User question
          |
          v
 Evidence + instructions
          |
          v
  LLM generation
          |
          v
 Draft + retrieved sources
          |
          v
     Human review
```

## Quick start

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run retrieval and inspect the grounded prompt

This mode does not require an API key:

```bash
python -m src.main --question "Describe the property's accessibility"
```

### 3. Generate a draft with an LLM

Set an API key and run:

```bash
export OPENAI_API_KEY="your-api-key"   # Windows PowerShell: $env:OPENAI_API_KEY="your-api-key"
python -m src.main --question "Describe the property's accessibility" --generate
```

The example uses the OpenAI Python SDK and a configurable model name. Review API pricing and data-handling requirements before using any real documents.

## Example output

For the question:

> Describe the property's accessibility.

The retriever should return source passages mentioning the nearby bus stop, road access, and parking. The generated draft should use only those facts. If the evidence does not contain a requested detail, the prompt instructs the model to say that the information is unavailable rather than inventing it.

## Project structure

```text
.
├── data/
│   └── sample_documents.json
├── examples/
│   └── algorithm_walkthrough.md
├── src/
│   ├── __init__.py
│   ├── chunking.py
│   ├── retrieval.py
│   ├── prompting.py
│   ├── generation.py
│   └── main.py
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── README.md
```

## Design decisions

- **Small, inspectable chunks:** makes it easier to retrieve specific facts and trace them back to their source.
- **Retrieval before generation:** the model receives relevant evidence instead of being asked to rely on general knowledge.
- **Sources returned with the draft:** reviewers can check where statements came from.
- **Human approval:** generated text is a starting point, not a final valuation or professional judgment.
- **Text generation:** retrieval can be tested independently of an LLM provider.

## Evaluation and original project context

In my MSc graduation project, I compared prompting configurations using a set of factual questions and evaluated the resulting outputs. The best-performing configuration achieved **0.89 accuracy in that project-specific evaluation**. This number refers to the original experiment; it is not a benchmark result for this small public demo.

For a next iteration, I would:
- define a more detailed evaluation rubric and report per-section results;
- add automated checks for unsupported claims and missing evidence;
- retain source identifiers at sentence level;
- test retrieval quality separately from generation quality;
- evaluate on a broader, carefully anonymized document set.

## Limitations

This implementation focuses on demonstrating the core RAG workflow rather than providing a production-ready valuation tool. TF-IDF is used to keep the demo lightweight. A production system may use domain-appropriate embedding models and a vector database. The sample documents are synthetic. The output must always be checked by a qualified human.

## Technologies

Python, retrieval-augmented generation, scikit-learn, OpenAI Python SDK ( ), prompt engineering, evaluation.
