from __future__ import annotations

import pandas as pd
import streamlit as st

from mapper import MAX_EVIDENCE_ITEMS, MAX_INPUT_CHARS, MAX_REQUIREMENTS, extract_evidence, extract_requirements, map_evidence, summary
from report import reviewed_to_csv, reviewed_to_markdown

st.set_page_config(page_title="Job Evidence Mapper", page_icon="🧭", layout="wide")

SAMPLE_REQUIREMENTS = """Build reliable Python applications
Design and integrate REST APIs
Write automated tests and debug production issues
Use Git and GitHub in a collaborative workflow
Communicate technical work to non-technical stakeholders"""

SAMPLE_EVIDENCE = """Built and deployed four Python and Streamlit applications with input validation
Created API-connected agent workflows during an Agentic AI professional certificate
Wrote pytest regression tests for file conversion and scientific auditing tools
Published documented projects in GitHub repositories with clear README files
Explained science concepts to pupils and collaborated with teachers and parents"""


def load_sample() -> None:
    st.session_state.requirements = SAMPLE_REQUIREMENTS
    st.session_state.evidence = SAMPLE_EVIDENCE
    st.session_state.pop("matches", None)


def clear_inputs() -> None:
    st.session_state.requirements = ""
    st.session_state.evidence = ""
    st.session_state.pop("matches", None)

st.title("Job Evidence Mapper")
st.caption("Turn a job advert and your real experience into a transparent evidence map.")

st.warning(
    "Use anonymised, non-sensitive text. Do not paste names, contact details, employer secrets, "
    "medical information or other confidential material. Text is used during the active session; "
    "the app does not intentionally save it, although hosting may create operational metadata."
)

with st.expander("What this tool does—and does not do", expanded=False):
    st.write(
        "It uses semantic sentence embeddings to suggest the closest evidence for each requirement. "
        "It does not decide whether you are suitable, rank you against other applicants, rewrite facts, "
        "or guarantee an interview. Every result requires human review."
    )

if "requirements" not in st.session_state:
    st.session_state.requirements = ""
if "evidence" not in st.session_state:
    st.session_state.evidence = ""

left, right = st.columns(2)
with left:
    st.subheader("1. Job requirements")
    st.text_area(
        "Paste one requirement per line",
        height=290,
        max_chars=MAX_INPUT_CHARS,
        key="requirements",
        placeholder="Example: Build reliable Python applications",
    )
with right:
    st.subheader("2. Your evidence")
    st.text_area(
        "Add one truthful example per line",
        height=290,
        max_chars=MAX_INPUT_CHARS,
        key="evidence",
        placeholder="Example: Built and deployed a Python Streamlit app with tests",
    )

sample_col, clear_col, analyse_col = st.columns([1, 1, 2])
with sample_col:
    st.button("Load fictional sample", width="stretch", on_click=load_sample)
with clear_col:
    st.button("Clear", width="stretch", on_click=clear_inputs)
with analyse_col:
    analyse = st.button("Map my evidence", type="primary", width="stretch")

if analyse:
    try:
        requirements = extract_requirements(st.session_state.requirements)
        evidence = extract_evidence(st.session_state.evidence)
        with st.spinner("Comparing requirements with your evidence by meaning..."):
            st.session_state.matches = map_evidence(requirements, evidence)
        if len(requirements) == MAX_REQUIREMENTS:
            st.info(f"Analysed the first {MAX_REQUIREMENTS} requirements.")
        if len(evidence) == MAX_EVIDENCE_ITEMS:
            st.info(f"Analysed the first {MAX_EVIDENCE_ITEMS} evidence examples.")
    except ValueError as exc:
        st.error(str(exc))

matches = st.session_state.get("matches")
if matches:
    counts = summary(matches)
    st.divider()
    st.subheader("3. Review the suggested map")
    a, b, c, d = st.columns(4)
    a.metric("Requirements", len(matches))
    b.metric("Supported", counts["Supported"])
    c.metric("Possible evidence", counts["Possible evidence"])
    d.metric("Gaps to review", counts["Gap to review"])

    st.info(
        "Semantic similarity compares meaning, not just identical words. It is still a suggestion—not a "
        "suitability score. Check every row yourself before using the evidence."
    )
    rows = [match.to_dict() for match in matches]
    frame = pd.DataFrame(rows).rename(
        columns={
            "requirement": "Requirement",
            "evidence": "Closest evidence",
            "similarity": "Semantic similarity",
            "status": "Suggested status",
            "explanation": "Why it matched",
        }
    )
    frame["Human decision"] = "Review"
    edited = st.data_editor(
        frame,
        hide_index=True,
        width="stretch",
        disabled=["Requirement", "Closest evidence", "Semantic similarity", "Suggested status", "Why it matched"],
        column_config={
            "Semantic similarity": st.column_config.ProgressColumn(min_value=0.0, max_value=1.0, format="%.2f"),
            "Human decision": st.column_config.SelectboxColumn(options=["Review", "Accept", "Replace evidence", "Not applicable"]),
        },
    )
    reviewed_rows = edited.to_dict(orient="records")

    export_left, export_right = st.columns(2)
    export_left.download_button(
        "Download evidence map (CSV)",
        data=reviewed_to_csv(reviewed_rows),
        file_name="job_evidence_map.csv",
        mime="text/csv",
        width="stretch",
    )
    export_right.download_button(
        "Download review notes (Markdown)",
        data=reviewed_to_markdown(reviewed_rows),
        file_name="job_evidence_review.md",
        mime="text/markdown",
        width="stretch",
    )

    st.subheader("Next actions")
    st.write("1. Replace weak matches with a more specific, truthful example if you have one.")
    st.write("2. Add numbers, outcomes or links only when you can verify them.")
    st.write("3. Treat genuine gaps as a learning plan—not an invitation to exaggerate.")
    st.write("4. Ask a person who understands the role to review the final evidence.")

st.caption("Job Evidence Mapper · Semantic matching · No paid AI API · Human review required")
