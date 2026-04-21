# TaskFlow

A task management app with AI-powered priority suggestions.

**Stack:** Python 3.11 + Flask · React 18 + TypeScript · SQLite (dev) / PostgreSQL (prod)

---

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env          # edit as needed
python run.py
```

API runs at `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm start
```

UI runs at `http://localhost:3000` (proxies `/api` to Flask)

### Run Tests

```bash
cd backend
pytest -v
```

---

## Key Technical Decisions

### 1. SQLite for dev, PostgreSQL-ready for prod
SQLAlchemy abstracts the DB layer entirely. Switching to Postgres is one env var change:
```
DATABASE_URL=postgresql://user:pass@host/dbname
```

### 2. Marshmallow for input validation
All API inputs are validated at the boundary before touching the DB. This prevents invalid
states from ever reaching the model layer. Validation errors return structured 422 responses.

### 3. AI priority with heuristic fallback
The AI feature (OpenAI GPT-4o-mini) is entirely optional. If `OPENAI_API_KEY` is not set,
the service falls back to keyword + due-date heuristics. The app is fully functional without
a paid API key.

### 4. Enum types for constrained values
`TaskStatus` and `Priority` are Python enums stored as SQLAlchemy Enum columns. This prevents
invalid values at the DB level as a second line of defense after schema validation.

### 5. Structured JSON logging
All log output is JSON-formatted for easy ingestion by log aggregators (Datadog, CloudWatch, etc.).
Failures are always logged with context before returning generic error messages to clients.

### 6. Pagination on list endpoints
The `/api/tasks/` endpoint always paginates (default 20/page, max 100). This prevents
unbounded queries as the dataset grows.

---

## Architecture

```
taskflow/
├── backend/
│   ├── app/
│   │   ├── __init__.py        # App factory, CORS, logging setup
│   │   ├── config.py          # Config classes (Config, TestConfig)
│   │   ├── database.py        # SQLAlchemy instance
│   │   ├── models.py          # Task, Tag, enums
│   │   ├── schemas.py         # Marshmallow validation schemas
│   │   ├── routes/
│   │   │   ├── tasks.py       # CRUD + filter + AI priority
│   │   │   ├── tags.py        # Tag management
│   │   │   └── health.py      # /api/health liveness probe
│   │   └── services/
│   │       └── ai_service.py  # OpenAI + heuristic fallback
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_tasks.py
│   │   ├── test_tags.py
│   │   └── test_ai_service.py
│   ├── run.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── types.ts            # Shared TypeScript types
│       ├── api.ts              # Typed API client
│       ├── hooks/              # useTasks, useTags
│       ├── components/         # TaskCard, TaskForm, Modal, Filters, Badges
│       └── App.tsx
├── agents.md                   # AI agent guidance (this file governs AI usage)
├── .env.example
└── README.md
```

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Liveness + DB check |
| GET | `/api/tasks/` | List tasks (filter, search, paginate) |
| POST | `/api/tasks/` | Create task (optional AI priority) |
| GET | `/api/tasks/:id` | Get single task |
| PATCH | `/api/tasks/:id` | Update task |
| DELETE | `/api/tasks/:id` | Delete task |
| GET | `/api/tags/` | List tags |
| POST | `/api/tags/` | Create tag |
| DELETE | `/api/tags/:id` | Delete tag |

Query params for `GET /api/tasks/`: `status`, `priority`, `tag_id`, `search`, `page`, `per_page`

---

## AI Usage

AI is used in two ways in this project:

1. **Feature**: `POST /api/tasks/` with `use_ai_priority: true` calls GPT-4o-mini to suggest
   a priority level and one-sentence reason based on the task title, description, and due date.

2. **Development**: Kiro (AI IDE) was used to scaffold the project. All generated code was
   reviewed against the constraints in `agents.md` before being accepted.

The prompt sent to OpenAI is documented in `backend/app/services/ai_service.py`. It requests
a strict JSON response to make parsing deterministic and safe.

---

## Risks & Tradeoffs

| Risk | Mitigation |
|------|-----------|
| OpenAI API unavailable | Heuristic fallback always runs |
| OpenAI returns unexpected JSON | `json.loads` + key validation; falls back to heuristics on any exception |
| SQLite not suitable for concurrent writes | Swap `DATABASE_URL` for Postgres in prod |
| No auth | Intentional for this assessment scope; `agents.md` flags it as requiring security review before adding |
| Frontend has no test suite | Would add React Testing Library tests as next step |

---

## Extension Approach

- **Auth**: Add Flask-JWT-Extended; all routes get `@jwt_required()`. Noted in `agents.md` as needing security review.
- **Recurring tasks**: Add `recurrence_rule` field (iCal RRULE string) + a background job (APScheduler/Celery).
- **Notifications**: Webhook or email via due-date background scan.
- **Postgres migration**: Change `DATABASE_URL`; add Flask-Migrate for schema migrations.
- **More AI**: Summarize overdue tasks, auto-suggest tags from description.
