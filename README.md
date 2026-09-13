# Job Evidence Mapper

Job Evidence Mapper helps job seekers compare role requirements with their own truthful, anonymised evidence. It produces an explainable preparation map rather than an opaque “job fit” score.

## Why this project exists

Generic resume tools often optimise keywords or return an unexplained percentage. This app keeps the human in control: each requirement is paired with the closest user-provided example, shared terms are displayed, gaps remain visible, and the tool never invents experience.

## MVP features

- Paste up to 30 job requirements and 40 evidence examples.
- Deterministic TF-IDF and cosine-similarity matching.
- Supported, possible-evidence and gap-to-review labels.
- Explanation for every suggested match.
- Manual review field in the interface.
- CSV and Markdown downloads.
- Human review decisions are preserved in both downloads.
- Fictional sample data and regression tests.
- No account, database or paid API key.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
pytest -q
```

## Deploy on Streamlit Community Cloud

1. Fork or upload this repository to GitHub.
2. In Streamlit Community Cloud, choose **Create app**.
3. Select the repository, the `main` branch, and `app.py` as the entry point.
4. Deploy. No secrets or API keys are required.

## Skills demonstrated

Python · Streamlit · scikit-learn · explainable matching · input validation · privacy-aware design · pytest · CSV/Markdown export

## Privacy and limitations

- Use anonymised, non-sensitive inputs only.
- The app does not intentionally persist submitted text. A hosting platform may still create operational metadata.
- Similarity is a heuristic text signal, not proof of competence or suitability.
- The app does not make hiring decisions, rank candidates or guarantee outcomes.
- Every match must be reviewed and corrected by the user.

## Technical design

The matcher splits newline-delimited requirements and evidence, creates word and bigram TF-IDF vectors, calculates cosine similarity, and proposes the closest evidence item for each requirement. Status thresholds are deliberately inspectable and covered by regression tests.

## Next iteration

- Improve requirement extraction from long-form job adverts.
- Let users add a short STAR evidence structure.
- Add a local semantic model only after measuring whether it improves matches.
- Conduct usability testing with job seekers and career changers.
