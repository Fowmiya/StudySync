import os

import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.database import Base, get_db
from app.main import app

# Import all models so SQLAlchemy knows about every table.
from app.db import models


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


# Create a separate database URL for automated tests.
TEST_DATABASE_URL = make_url(DATABASE_URL).set(
    database="studysync_test"
)


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_size=1,
        max_overflow=0,
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

        await connection.execute(
            text(
                """
                TRUNCATE TABLE
                    study_sessions,
                    performance_records,
                    tasks,
                    subjects,
                    users
                RESTART IDENTITY CASCADE
                """
            )
        )

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_engine):
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def override_get_db():
        async with TestSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(
        app=app,
        raise_app_exceptions=False
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()