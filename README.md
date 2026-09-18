# Job Evidence Mapper

A privacy-aware Streamlit application that maps job requirements to a candidate's truthful evidence and makes gaps explicit—without inventing experience or hiding the reasoning behind a score.

## The problem

Generic résumé tools often optimise keywords or return an unexplained match percentage. Career changers need something more useful: a requirement-by-requirement preparation map showing what evidence exists, what might be relevant and what still needs work.

## What the application does

- accepts up to 30 job requirements and 40 evidence examples
- matches requirements to evidence with sentence-transformer embeddings and cosine similarity
- labels results as **supported**, **possible evidence** or **gap to review**
- shows shared terms and an explanation for every suggested match
- preserves human review decisions
- exports results as CSV and Markdown
- includes fictional sample data and regression tests
- requires no account, database or paid API key

## How it works

```text
Job requirements ─┐
                  ├─ validation → sentence embeddings → cosine similarity
User evidence ────┘                                  ↓
                         explainable match → human review → CSV/Markdown
```

The system uses the pretrained `all-MiniLM-L6-v2` sentence-transformer model locally on the application host. The model is cached in memory after a successful load. First use may download model files; submitted text is encoded on the host, not sent to a paid AI API. Similarity is treated as a decision-support signal, never as proof of competence or suitability.

## Tech stack

Python · Streamlit · sentence-transformers · scikit-learn · pandas · pytest · GitHub Actions

## Run locally

```bash
git clone https://github.com/kalpanaiitm/job-evidence-mapper.git
cd job-evidence-mapper
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
pytest -q
```

## Design decisions

- **Inspection:** each match shows its similarity score and any shared terms. Shared terms are not a faithful explanation of the embedding model's reasoning.
- **Privacy:** inputs are not intentionally persisted by the application.
- **Human control:** users can review and correct every match.
- **Truthfulness:** gaps remain visible; the tool never manufactures experience.
- **Evaluation:** regression tests cover basic matching, parsing, exports, model reuse and UI result invalidation. They are not a benchmark of matching accuracy.

## Limitations

- semantic similarity can miss negation, differences in seniority and incomplete or exaggerated evidence
- thresholds are heuristic and not calibrated probabilities; a high similarity score does not establish competence
- the tool does not rank candidates or make hiring decisions
- hosting providers may retain operational metadata

Use anonymised, non-sensitive inputs and review every output.

## Next iteration

- extract requirements from long-form job adverts
- add optional STAR evidence fields
- build a labelled evaluation set including paraphrases, negation and misleading overlap; compare the semantic model with a TF-IDF baseline
- add usability testing with career changers

## About the builder

Created by Dr Kalpana Govindarasan, a scientist and educator transitioning into applied AI. The project reflects a focus on explainable systems, responsible use and practical tools for real users.

