"""Deterministic requirement-to-evidence matching for Job Evidence Mapper."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MAX_REQUIREMENTS = 30
MAX_EVIDENCE_ITEMS = 40
MAX_INPUT_CHARS = 20_000


@dataclass(frozen=True)
class Match:
    requirement: str
    evidence: str
    similarity: float
    status: str
    explanation: str

    def to_dict(self) -> dict:
        return asdict(self)


def _normalise_line(text: str) -> str:
    text = re.sub(r"^\s*(?:[-*•]+|\d+[.)])\s*", "", text)
    return re.sub(r"\s+", " ", text).strip(" .;:\t")


def parse_items(text: str, limit: int) -> list[str]:
    """Parse newline/bullet text into unique, bounded items."""
    if len(text) > MAX_INPUT_CHARS:
        raise ValueError(f"Input is longer than {MAX_INPUT_CHARS:,} characters.")
    items: list[str] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        item = _normalise_line(raw)
        key = item.casefold()
        if len(item) >= 3 and key not in seen:
            items.append(item)
            seen.add(key)
        if len(items) >= limit:
            break
    return items


def extract_requirements(text: str) -> list[str]:
    return parse_items(text, MAX_REQUIREMENTS)


def extract_evidence(text: str) -> list[str]:
    return parse_items(text, MAX_EVIDENCE_ITEMS)


def _shared_terms(left: str, right: str) -> list[str]:
    stop = {
        "and", "the", "with", "for", "that", "this", "from", "your", "you",
        "using", "have", "has", "are", "our", "will", "into", "years", "year",
        "in", "to", "of", "on", "at", "by", "as", "an", "a", "or",
    }

    irregular = {"built": "build", "wrote": "write", "written": "write"}

    def canonical(token: str) -> str:
        token = irregular.get(token, token)
        if token.endswith("ies") and len(token) > 4:
            return token[:-3] + "y"
        if token.endswith("s") and not token.endswith("ss") and len(token) > 4:
            return token[:-1]
        return token

    tokens = lambda s: {
        canonical(t)
        for t in re.findall(r"[a-z0-9+#.-]{2,}", s.lower())
        if t not in stop
    }
    return sorted(tokens(left) & tokens(right))


def _status(score: float, shared: Iterable[str]) -> str:
    shared_count = len(list(shared))
    if score >= 0.34 or shared_count >= 2:
        return "Supported"
    if score >= 0.14 or shared_count >= 1:
        return "Possible evidence"
    return "Gap to review"


def map_evidence(requirements: list[str], evidence_items: list[str]) -> list[Match]:
    if not requirements:
        raise ValueError("Add at least one job requirement.")
    if not evidence_items:
        raise ValueError("Add at least one evidence example.")

    corpus = requirements + evidence_items
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True, sublinear_tf=True)
    matrix = vectorizer.fit_transform(corpus)
    req_matrix = matrix[: len(requirements)]
    evidence_matrix = matrix[len(requirements) :]
    similarities = cosine_similarity(req_matrix, evidence_matrix)

    matches: list[Match] = []
    for index, requirement in enumerate(requirements):
        best_index = int(similarities[index].argmax())
        score = float(similarities[index, best_index])
        evidence = evidence_items[best_index]
        shared = _shared_terms(requirement, evidence)
        status = _status(score, shared)
        if shared:
            explanation = "Shared terms: " + ", ".join(shared[:8])
        else:
            explanation = "No strong shared terms; review manually."
        matches.append(Match(requirement, evidence, round(score, 3), status, explanation))
    return matches


def summary(matches: list[Match]) -> dict[str, int]:
    counts = {"Supported": 0, "Possible evidence": 0, "Gap to review": 0}
    for match in matches:
        counts[match.status] += 1
    return counts
