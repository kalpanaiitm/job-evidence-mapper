# Project blueprint — job-evidence-mapper

## Problem and scope
Career changers matching job criteria to truthful evidence. The current repository scope is described by its README and implemented files.

## Architecture and contracts
Line-based requirements and evidence → local sentence embeddings → cosine similarity and heuristic status → human review → CSV/Markdown. User content is untrusted data. Errors should be shown without disclosing private contents.

## Ground truth and review
Outputs must be checked against the input document, audio, or user-supplied evidence. No automated score proves scientific correctness or job suitability.

## Known limits
Model scores are not probabilities; negation and seniority can fool matching.

## Next milestone and acceptance
Labelled paraphrase/negation set and TF-IDF baseline; record precision and failure cases. The milestone is complete only when its implementation, meaningful tests, and measured results are committed.

## Release gate
Run automated tests, inspect realistic end-to-end output, record actual failures and limitations, and update the README before claiming the milestone.
