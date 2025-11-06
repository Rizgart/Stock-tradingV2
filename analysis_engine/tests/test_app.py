import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from analysis_engine.app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_recommendations_endpoint_returns_data() -> None:
    response = client.get("/recommendations", params={"tickers": "AAPL,TSLA", "lookback_days": 45})
    assert response.status_code == 200
    body = response.json()
    assert body["results"]
    first = body["results"][0]
    assert {"ticker", "score", "signal", "reasoning"}.issubset(first.keys())
    assert body["disclaimer"]
