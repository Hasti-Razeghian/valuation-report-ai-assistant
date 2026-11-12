# Algorithm walkthrough

The core workflow can be summarized as:

```text
INPUT: source documents D, user question q

1. Extract text from each document.
2. Split the text into overlapping chunks.
3. Convert chunks into searchable representations.
4. Convert q into the same representation.
5. Rank chunks by similarity to q.
6. Select the top-k relevant passages.
7. Construct a prompt containing q, evidence, and grounding rules.
8. Optionally generate a draft with an LLM.
9. Return the draft and its source passages for human review.

OUTPUT: evidence-grounded draft + traceable source passages
```

## Why these steps?

**Chunking:** whole documents may contain too much unrelated information. Smaller chunks make retrieval more focused.

**Retrieval:** the model should receive relevant source material rather than being asked to recall facts from its general training.

**Grounded generation:** explicit instructions tell the model not to fill gaps with assumptions.

**Review:** retrieval and prompting reduce some risks, but they do not guarantee correctness. A person must verify the draft against the source material.
