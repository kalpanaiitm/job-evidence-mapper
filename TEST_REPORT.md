# Test report

## Scope
This report distinguishes automated tests from an end-to-end or deployed demonstration. A passing unit test does not prove model quality, document fidelity, or deployment reliability.

## Current verification
The repository contains model-backed matching, parsing, export, and UI-state tests, plus a GitHub Actions workflow. The local result is below; no deployed end-to-end or matching-quality evaluation was performed.

## Remaining evaluation
Labelled paraphrase/negation set and TF-IDF baseline; record precision and failure cases.

## Local run, 2026-09-28
`HF_HUB_OFFLINE=1 python -m pytest -q` → **13 passed, 4 failed**. The four model-backed matching tests could not load the sentence-transformer model in this offline environment (HTTP proxy lacks `socksio`); they did not establish an application defect or a pass. Run the full suite in an environment that can download/cache `all-MiniLM-L6-v2`, and retain the result here. The existing GitHub Actions workflow has not been verified in this review.

## Retest with model available
After installing the missing local SOCKS transport dependency and allowing the model download, `python -m pytest -q` → **17 passed in 43.29s** (2026-09-28). This resolves the earlier environment failure. Matching accuracy on a labelled evaluation set remains unmeasured.
