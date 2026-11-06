# Leaderboard API

Small FastAPI app: a community-event leaderboard. In-memory store, no database.

## Commands
- Test: the TEST_CMD in factory.conf (must pass before any PR)
- Lint: the LINT_CMD in factory.conf

## Conventions
- Python 3.10+, FastAPI, type hints everywhere.
- Every endpoint gets a pytest test in `tests/`, written BEFORE the implementation.
- Keep functions under 30 lines. No new dependencies: requirements.txt is protected.
- State lives in `app/store.py` only. Endpoints never hold state.

## Factory rules
- Phase state lives in `.factory/` as markdown files. Never put plan or review text in code comments.
- Only the paths in SCOPE (factory.conf) may change. Do not touch factory.sh, lib/, gates/, prompts/ or this file.
- Security: no eval/exec, no shell calls from endpoints, validate all inputs with pydantic.
