import pytest

from mapper import extract_evidence, extract_requirements, map_evidence, summary
from report import reviewed_to_csv, reviewed_to_markdown, to_csv, to_markdown


def test_parses_bullets_and_removes_duplicates():
    text = "- Python development\n• API design\n1. Python development\n"
    assert extract_requirements(text) == ["Python development", "API design"]


def test_maps_obvious_evidence_as_supported():
    matches = map_evidence(
        ["Build Python applications with automated testing"],
        ["Built Python applications and wrote automated tests with pytest"],
    )
    assert matches[0].status == "Supported"
    assert matches[0].similarity > 0


def test_flags_unrelated_evidence_for_review():
    matches = map_evidence(
        ["Design REST APIs"],
        ["Taught secondary school chemistry"],
    )
    assert matches[0].status == "Gap to review"


def test_common_connecting_words_do_not_create_a_match():
    matches = map_evidence(
        ["Communicate technical work to non-technical stakeholders"],
        ["Travelled to a conference in London"],
    )
    assert matches[0].status == "Gap to review"


def test_empty_inputs_are_rejected():
    with pytest.raises(ValueError):
        map_evidence([], ["Evidence"])


def test_exports_include_guardrail_and_rows():
    matches = map_evidence(["Use GitHub"], ["Published projects on GitHub"])
    assert "requirement,status,evidence" in to_csv(matches)
    assert "not a hiring decision" in to_markdown(matches)
    assert summary(matches)[matches[0].status] == 1


def test_reviewed_exports_preserve_human_decision():
    rows = [{
        "Requirement": "Use GitHub",
        "Closest evidence": "Published projects on GitHub",
        "Text similarity": 0.5,
        "Suggested status": "Supported",
        "Why it matched": "Shared terms: github",
        "Human decision": "Accept",
    }]
    assert "Accept" in reviewed_to_csv(rows)
    assert "Human decision: Accept" in reviewed_to_markdown(rows)

def test_short_skills_are_preserved():
    assert extract_requirements("R\nC#\nGo\nSQL\nR\n---") == ["R", "C#", "Go", "SQL"]


def test_input_limits_and_empty_evidence():
    from mapper import MAX_INPUT_CHARS, MAX_REQUIREMENTS
    with pytest.raises(ValueError):
        extract_requirements("x" * (MAX_INPUT_CHARS + 1))
    assert len(extract_requirements("\n".join(f"Skill {i}" for i in range(40)))) == MAX_REQUIREMENTS
    with pytest.raises(ValueError):
        map_evidence(["Python"], [])


def test_model_is_reused(monkeypatch):
    import mapper
    calls = []
    sentinel = object()
    def factory(name):
        calls.append(name)
        return sentinel
    mapper._model.cache_clear()
    monkeypatch.setattr(mapper, "SentenceTransformer", factory)
    try:
        assert mapper._model() is mapper._model() is sentinel
        assert len(calls) == 1
    finally:
        mapper._model.cache_clear()


def test_failed_model_load_can_be_retried(monkeypatch):
    import mapper
    calls = []
    def factory(name):
        calls.append(name)
        if len(calls) == 1:
            raise OSError("offline")
        return object()
    mapper._model.cache_clear()
    monkeypatch.setattr(mapper, "SentenceTransformer", factory)
    try:
        with pytest.raises(OSError):
            mapper._model()
        assert mapper._model() is not None
        assert len(calls) == 2
    finally:
        mapper._model.cache_clear()


def test_semantic_column_is_exported():
    rows = [{"Requirement": "R", "Closest evidence": "Used R",
             "Semantic similarity": 0.75, "Suggested status": "Supported",
             "Why it matched": "Review manually", "Human decision": "Accept"}]
    assert "Semantic similarity: 0.75" in reviewed_to_markdown(rows)

