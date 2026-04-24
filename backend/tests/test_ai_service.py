from datetime import datetime, timezone, timedelta
from app.services.ai_service import _heuristic_priority


def test_heuristic_critical_keyword():
    priority, reason = _heuristic_priority("URGENT outage", None, None)
    assert priority == "critical"


def test_heuristic_high_keyword():
    priority, reason = _heuristic_priority("Fix security bug", None, None)
    assert priority == "high"


def test_heuristic_low_keyword():
    priority, reason = _heuristic_priority("Nice to have feature", None, None)
    assert priority == "low"


def test_heuristic_overdue():
    past = datetime.now(timezone.utc) - timedelta(days=1)
    priority, reason = _heuristic_priority("Some task", None, past)
    assert priority == "critical"
    assert "overdue" in reason.lower()


def test_heuristic_due_soon():
    soon = datetime.now(timezone.utc) + timedelta(hours=12)
    priority, reason = _heuristic_priority("Some task", None, soon)
    assert priority == "critical"


def test_heuristic_due_in_week():
    week = datetime.now(timezone.utc) + timedelta(days=5)
    priority, reason = _heuristic_priority("Some task", None, week)
    assert priority == "medium"


def test_heuristic_default():
    priority, reason = _heuristic_priority("Write a blog post", None, None)
    assert priority == "medium"


def test_suggest_priority_falls_back_on_import_error(monkeypatch):
    """If openai is not importable, suggest_priority should fall back to heuristics."""
    import builtins
    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "openai":
            raise ImportError("openai not installed")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)

    from app.services.ai_service import suggest_priority
    priority, reason = suggest_priority("URGENT fix", None, None, api_key="fake-key")
    assert priority in ("critical", "high", "medium", "low")
    assert reason is not None
