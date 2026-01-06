# FastAPI Starter (async)

A basic Starter Kit for async FastAPI - without the fluff.
Debloated 3-Environment Setup with async sqlalchemy integration.
ENV-management with the handy pydantic-settings package.
Starting with 3 local sqlite DBs via aiosqlite-connector. (development, testing, production).
The template follows common best-practices and is an optimal starting point.

## What's in it?

- 3 Stages / ENVIRONMENTs: development, testing, production
- FastAPI with GZipMiddleware
- SQLite (async sqlite-Connector "aiosqlite")
- real async DB-logic with sqlalchemy
- uvicorn with uvloop (faster async)
- logging (updated and with new metaclass approach)
- prod-ready folder structure
- pytest, pytest-asyncio, pytest-env & httpx for Tests
- CRUD-Tests (Unit Tests) & Route-Tests (Integration Tests)

## ! Important !
- a real PW Hashing function is missing: this is just for demonstrational purposes

## Installation
Prerequisite: [uv](https://github.com/astral-sh/uv)
- `uv sync`
- rename example.env to .env and add external DB credentials and API-Key (optional)
- For Production you should at least switch the corresponding production-DB to mySQL (`uv add aiomysql`) or Postgres (`uv add asyncpg`)

## USAGE
- in your .env file: set your environment to development (default) or production
- start your api via
```bash
uv ru` python main.py
# or directly
uv run fastapi dev src/main.py
```


## TEST DEMO
Testing is fully automated. You do not need to change your .env file!
The setup automatically switches to a temporary test.db and prevents data loss in development. After the Tests db is cleared completely for a fresh start.
- mock tests for user endpoint (unit and integration)
- for testing simply type `pytest -v` or `pytest -vv -rA` (more details) in your project root
- or use with uv (`uv run pytest -v` or `uv run pytest -vv -rA`)

## TODO

- add alembic
