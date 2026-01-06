import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from src.config import SET_CONF
from src.database import Base, get_db_session_local
from src.load_app import app

TEST_DATABASE_URL = SET_CONF.SQLALCHEMY_DATABASE_URI


@pytest.fixture
async def test_engine():
    """
    new engine for every test
    no scope="session" -> preventing event loop conflicts.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_db_session(test_engine):
    """
    Session creation
    """
    async_session_maker = async_sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session_maker() as session:
        yield session
        # Optional: Explizites Rollback am Ende, falls der Test crasht
        await session.rollback()


@pytest.fixture
async def client(test_db_session):
    """
    HTTP Client with DB-Override.
    """

    async def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db_session_local] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
