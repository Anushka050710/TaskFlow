# AI Agent Guidance — TaskFlow

This file defines constraints and standards for AI agents (Kiro, Copilot, Claude, etc.)
working on this codebase.

---

## Project Context

TaskFlow is a task management app with:
- **Backend**: Python 3.11 + Flask + SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **Frontend**: React 18 + TypeScript (strict mode)
- **AI feature**: Priority suggestion via OpenAI GPT-4o-mini with heuristic fallback

---

## Hard Rules (never violate)

1. **No raw SQL** — always use SQLAlchemy ORM or `text()` with bound parameters.
2. **Validate all inputs** at the API boundary using Marshmallow schemas before touching the DB.
3. **Never expose stack traces** to API consumers — log internally, return generic error messages.
4. **No secrets in code** — use `os.environ.get(...)` with safe defaults.
5. **TypeScript strict mode** — no `any` types unless absolutely unavoidable and commented.
6. **All new API routes** must have at least one happy-path and one error-path test.
7. **AI service must always have a fallback** — the app must work without an OpenAI key.

---

## Code Style

### Python
- Follow PEP 8; max line length 100.
- Use type hints on all function signatures.
- Prefer explicit `return` types.
- Use `current_app.logger` for logging — never `print()`.
- Enums for constrained string values (TaskStatus, Priority).

### TypeScript / React
- Functional components only — no class components.
- Props interfaces defined inline or in `types.ts`.
- Custom hooks in `src/hooks/` — one concern per hook.
- No inline styles for repeated patterns — extract to CSS or a shared style object.
- `aria-label` on all interactive elements that lack visible text.

---

## What AI Should NOT Do

- Do not add new dependencies without noting the reason in a comment or PR description.
- Do not change the database schema without a corresponding migration plan.
- Do not remove existing tests — only add or fix them.
- Do not use `eval()`, `exec()`, or dynamic imports from user input.
- Do not add authentication/authorization logic without a security review note.
- Do not silently swallow exceptions — always log or re-raise.

---

## Preferred Patterns

### Adding a new API resource
1. Add model to `backend/app/models.py`
2. Add schema to `backend/app/schemas.py`
3. Add route blueprint to `backend/app/routes/`
4. Register blueprint in `backend/app/__init__.py`
5. Add tests in `backend/tests/`

### Adding a new AI feature
1. Add logic to `backend/app/services/ai_service.py` or a new service file
2. Always implement a non-AI fallback
3. Wrap OpenAI calls in try/except and log failures
4. Document the prompt template in a docstring

---

## Testing Standards

- Use `pytest` with `pytest-flask`
- Test DB uses SQLite in-memory (`TestConfig`)
- Each test function is independent — no shared state
- Name tests: `test_<what>_<condition>` e.g. `test_create_task_missing_title`
