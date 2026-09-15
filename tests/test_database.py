import pytest
from unittest.mock import AsyncMock

import app.db.database as database


@pytest.mark.asyncio
async def test_get_db_rolls_back_on_error():
    mock_session = AsyncMock()

    class MockSessionContext:
        async def __aenter__(self):
            return mock_session

        async def __aexit__(self, exc_type, exc_value, traceback):
            return False

    original_session_local = database.AsyncSessionLocal

    try:
        database.AsyncSessionLocal = lambda: MockSessionContext()

        db_generator = database.get_db()

        session = await anext(db_generator)

        assert session is mock_session

        with pytest.raises(RuntimeError, match="Test database failure"):
            await db_generator.athrow(
                RuntimeError("Test database failure")
            )

        mock_session.rollback.assert_awaited_once()

    finally:
        database.AsyncSessionLocal = original_session_local