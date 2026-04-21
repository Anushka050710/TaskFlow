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
