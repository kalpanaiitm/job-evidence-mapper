from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest
import mapper

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def start(monkeypatch):
    monkeypatch.setattr(mapper, "map_evidence", lambda requirements, evidence: [
        mapper.Match(requirements[0], evidence[0], 0.75, "Supported", "Test match")
    ])
    app = AppTest.from_file(APP).run()
    app.text_area(key="requirements").set_value("Python").run()
    app.text_area(key="evidence").set_value("Built Python apps").run()
    next(b for b in app.button if b.label == "Map my evidence").click().run()
    assert not app.exception
    assert app.session_state["matches"]
    return app


@pytest.mark.parametrize("field", ["requirements", "evidence"])
def test_editing_inputs_invalidates_results(monkeypatch, field):
    app = start(monkeypatch)
    app.text_area(key=field).set_value("Different input").run()
    assert not app.exception
    assert "matches" not in app.session_state
    assert not app.metric


def test_model_failure_shows_friendly_error_and_clears_results(monkeypatch):
    app = start(monkeypatch)
    def fail(*args):
        raise OSError("download failure")
    monkeypatch.setattr(mapper, "map_evidence", fail)
    next(b for b in app.button if b.label == "Map my evidence").click().run()
    assert not app.exception
    assert "matches" not in app.session_state
    assert "could not load or run" in app.error[0].value


def test_invalid_input_leaves_no_results(monkeypatch):
    app = start(monkeypatch)
    app.text_area(key="evidence").set_value("").run()
    monkeypatch.setattr(mapper, "map_evidence", lambda r, e: (_ for _ in ()).throw(ValueError("Add evidence")))
    next(b for b in app.button if b.label == "Map my evidence").click().run()
    assert not app.exception
    assert "matches" not in app.session_state
    assert app.error


def test_clear_removes_results(monkeypatch):
    app = start(monkeypatch)
    next(b for b in app.button if b.label == "Clear").click().run()
    assert not app.exception
    assert "matches" not in app.session_state
    assert app.text_area(key="requirements").value == ""

