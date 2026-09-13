"""Export helpers for Job Evidence Mapper."""

from __future__ import annotations

import csv
import io
from collections.abc import Mapping, Sequence

from mapper import Match, summary


def to_csv(matches: list[Match]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["requirement", "status", "evidence", "similarity", "explanation"],
    )
    writer.writeheader()
    writer.writerows(match.to_dict() for match in matches)
    return output.getvalue()


def to_markdown(matches: list[Match]) -> str:
    counts = summary(matches)
    lines = [
        "# Job Evidence Review",
        "",
        "> This is a heuristic preparation aid, not a hiring decision or guarantee.",
        "",
        "## Summary",
        "",
        f"- Supported: {counts['Supported']}",
        f"- Possible evidence: {counts['Possible evidence']}",
        f"- Gaps to review: {counts['Gap to review']}",
        "",
        "## Evidence map",
        "",
    ]
    for index, item in enumerate(matches, start=1):
        lines += [
            f"### {index}. {item.requirement}",
            f"- Status: {item.status}",
            f"- Closest evidence: {item.evidence}",
            f"- Semantic similarity: {item.similarity}",
            f"- Why it matched: {item.explanation}",
            "- Human check: Confirm this example is truthful, specific and relevant.",
            "",
        ]
    return "\n".join(lines)


def reviewed_to_csv(rows: Sequence[Mapping[str, object]]) -> str:
    """Export the table exactly as reviewed in the Streamlit interface."""
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def reviewed_to_markdown(rows: Sequence[Mapping[str, object]]) -> str:
    """Create review notes that preserve the user's human decisions."""
    lines = [
        "# Job Evidence Review",
        "",
        "> This is a semantic matching preparation aid, not a hiring decision or guarantee.",
        "",
        "## Evidence map",
        "",
    ]
    for index, row in enumerate(rows, start=1):
        similarity = row.get("Semantic similarity", row.get("Text similarity", "N/A"))
        lines += [
            f"### {index}. {row['Requirement']}",
            f"- Suggested status: {row['Suggested status']}",
            f"- Human decision: {row['Human decision']}",
            f"- Closest evidence: {row['Closest evidence']}",
            f"- Semantic similarity: {similarity}",
            f"- Why it matched: {row['Why it matched']}",
            "",
        ]
    return "\n".join(lines)
