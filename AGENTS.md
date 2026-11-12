# Leaderboard API

Small FastAPI app: a community-event leaderboard. In-memory store, no database.

## Code layout
- `app/main.py`: the FastAPI `app`, pydantic input models (e.g. `ScoreIn`) and the endpoints:
  `GET /health`, `POST /scores` (adds points, returns the player's total),
  `GET /leaderboard?limit=` (top players, `limit` 1-100, else 422).
- `app/store.py`: `Store` class and the `STORE` singleton. The ONLY place state lives
  (`add`, `total`, `top`, `reset`). Reads must not create entries (`total` uses `.get`).
- `tests/test_main.py`: pytest + FastAPI `TestClient`. `setup_function` calls `STORE.reset()`
  so every test starts empty. Add new tests here (or new `tests/test_*.py` files) in the same style.
- Everything else (factory.sh, lib/, gates/, dashboard/, doctor.sh, .claude/) is the factory
  itself, not the app. Don't read it for app behavior and never edit it.

## Commands
Run from the repo root with the venv on PATH (`PATH_PREPEND="venv/bin"` in factory.conf):
- Test: `pytest -q -p no:cacheprovider` (TEST_CMD). Must pass before any PR.
- Lint: `ruff check --no-cache app tests` (LINT_CMD). Must be clean.
- If `venv/` is missing: `python3 -m venv venv && venv/bin/pip install -q -r requirements.txt`.
Always use the commands exactly as written in factory.conf; it wins if this file disagrees.

## Conventions
- Python 3.10+, FastAPI, type hints everywhere (including `-> None` on tests).
- TDD: every endpoint or behavior change gets a pytest test in `tests/`, written and seen
  failing BEFORE the implementation. Test behavior through HTTP, not internals.
- Keep functions under 30 lines.
- Endpoints never hold state: they call `STORE` methods. Add new store methods in `app/store.py`.
- Validate every input with pydantic (`Field` constraints) or explicit checks returning 422.

## What you must NOT change
- Only paths in SCOPE (factory.conf: `app/ tests/`) may change. Anything else rejects the run.
- Protected, never edit: `AGENTS.md`, `factory.sh`, `factory.conf`, `doctor.sh`, `.gitignore`,
  `requirements.txt`, `venv/`, and the dirs `lib/`, `gates/`, `dashboard/`, `.claude/`, `.git/`.
- No new dependencies (requirements.txt is protected). Use only fastapi, pydantic, stdlib.
- Don't break existing endpoints or their response shapes; existing tests must keep passing.
  Don't delete or weaken existing tests to make a change pass.

## Factory rules
- Phase state lives in `.factory/` as markdown (plan.md, build.md, report.md, review.md).
  Each phase writes only its own file. Never put plan or review text in code comments.
- Security: no eval/exec, no shell or subprocess calls, no file or network I/O from endpoints,
  no secrets in code or logs.
