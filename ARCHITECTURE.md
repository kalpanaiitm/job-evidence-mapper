# Architecture

Line-based requirements and evidence → local sentence embeddings → cosine similarity and heuristic status → human review → CSV/Markdown.

The README names the runnable entry point. Components should keep validation separate from the core operation and presentation. The existing code is the source of truth; this page does not claim planned capabilities as implemented.

## Failure and privacy boundaries
Model scores are not probabilities; negation and seniority can fool matching. Use non-sensitive or permitted inputs for demos. Do not commit user documents, audio, credentials, or generated outputs.
