# Test report

## Scope
This report distinguishes automated tests from an end-to-end or deployed demonstration. A passing unit test does not prove model quality, document fidelity, or deployment reliability.

## Current verification
See the tests and workflow (if present) in this repository. Execution results for the current revision must be recorded here after running them. No unrun test is represented as a pass.

## Remaining evaluation
Labelled paraphrase/negation set and TF-IDF baseline; record precision and failure cases.

## Local run, 2026-09-28
`HF_HUB_OFFLINE=1 python -m pytest -q` → **13 passed, 4 failed**. The four model-backed matching tests could not load the sentence-transformer model in this offline environment (HTTP proxy lacks `socksio`); they did not establish an application defect or a pass. Run the full suite in an environment that can download/cache `all-MiniLM-L6-v2`, and retain the result here. The existing GitHub Actions workflow has not been verified in this review.
