import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.study_tip_service import StudyTipServiceError


@pytest.mark.anyio
async def test_study_tip_route_uses_mocked_service(monkeypatch):
    async def mock_get_study_tip():
        return "Keep studying consistently."

    monkeypatch.setattr(
        "app.main.get_study_tip",
        mock_get_study_tip
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/study-tip")

    assert response.status_code == 200
    assert response.json() == {
        "study_tip": "Keep studying consistently."
    }


@pytest.mark.anyio
async def test_study_tip_service_failure_returns_503(monkeypatch):
    async def mock_get_study_tip():
        raise StudyTipServiceError(
            "Study tip service timed out"
        )

    monkeypatch.setattr(
        "app.main.get_study_tip",
        mock_get_study_tip
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/study-tip")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Study tip service timed out"
    }