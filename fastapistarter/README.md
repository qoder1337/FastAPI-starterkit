# FastAPI Starter (async)

A work in progress Starter Kit for async FastAPI without the fluff.
Debloated 3-Environment Setup with async sqlalchemy integration.
ENV-management with the handy pydantic-settings package.
Starting with 3 local sqlite DBs via aiosqlite-connector. (development, testing, production)

## Whats in it?

- 3 Stages / ENVIRONMENTs: development, testing, production
- real async DB-logic with sqlalchemy
- uvicorn with uvloop (faster async)
- logging
- prod-ready folder structure
- Dockerfile

## Installation
- uv sync
- rename example.env to .env and add external DB credentials and API-Key (optional)
- For Production you should at least switch the corresponding production-DB to mySQL (uv add aiomysql) or Postgres (uv add asyncpg).
- you might need: httpx (uv add httpx) - if you want to use the TestClient.

## TODO

- add alembic
