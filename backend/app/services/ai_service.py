"""
AI Priority Service
-------------------
Uses OpenAI (if key is configured) to suggest a priority level for a task
based on its title, description, and due date.

Falls back to rule-based heuristics when no API key is present so the app
works fully offline / without a paid key.
"""

import logging
import re
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

# Keywords that bump priority up
URGENCY_KEYWORDS = {
    "critical": ["critical", "urgent", "asap", "emergency", "blocker", "outage", "down"],
    "high": ["important", "deadline", "must", "required", "broken", "bug", "fix", "security"],
    "low": ["nice to have", "someday", "maybe", "optional", "low priority", "minor"],
}


def _heuristic_priority(title: str, description: Optional[str], due_date: Optional[datetime]) -> tuple[str, str]:
    """Rule-based fallback when OpenAI is unavailable."""
    text = f"{title} {description or ''}".lower()

    for priority, keywords in URGENCY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return priority, f"Keyword match: text contains urgency signals for '{priority}' priority."

    if due_date:
        now = datetime.now(timezone.utc)
        due = due_date if due_date.tzinfo else due_date.replace(tzinfo=timezone.utc)
        days_until = (due - now).days
        if days_until < 0:
            return "critical", "Task is overdue."
        if days_until <= 1:
            return "critical", "Due within 24 hours."
        if days_until <= 3:
            return "high", "Due within 3 days."
        if days_until <= 7:
            return "medium", "Due within a week."

    return "medium", "No strong urgency signals detected; defaulting to medium."


def suggest_priority(
    title: str,
    description: Optional[str],
    due_date: Optional[datetime],
    api_key: str = "",
) -> tuple[str, str]:
    """
    Returns (priority_level, reason_string).
    Tries OpenAI first; falls back to heuristics.
    """
    if api_key:
        try:
            return _openai_priority(title, description, due_date, api_key)
        except Exception as exc:
            logger.warning("OpenAI priority suggestion failed, using heuristics: %s", exc)

    return _heuristic_priority(title, description, due_date)


def _openai_priority(
    title: str,
    description: Optional[str],
    due_date: Optional[datetime],
    api_key: str,
) -> tuple[str, str]:
    try:
        import openai  # lazy import — optional dependency
    except ImportError as exc:
        raise ImportError("openai package is not installed; falling back to heuristics") from exc

    client = openai.OpenAI(api_key=api_key)

    due_str = due_date.isoformat() if due_date else "not set"
    prompt = (
        "You are a task prioritization assistant. "
        "Given the task details below, respond with ONLY a JSON object with two keys: "
        '"priority" (one of: low, medium, high, critical) and "reason" (one sentence explanation).\n\n'
        f"Title: {title}\n"
        f"Description: {description or 'N/A'}\n"
        f"Due date: {due_str}\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    import json
    data = json.loads(raw)
    priority = data["priority"].lower()
    reason = data["reason"]

    valid = {"low", "medium", "high", "critical"}
    if priority not in valid:
        raise ValueError(f"Unexpected priority value from AI: {priority}")

    return priority, reason
