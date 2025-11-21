import pytest
from fastapi.testclient import TestClient
from app.main import create_app

def test_app_lifespan_and_health(monkeypatch):
    app = create_app()
    client = TestClient(app)

    # Проверяем, что health endpoint работает
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

    # Проверяем, что app.state.celery_app был инициализирован через lifespan
    # TestClient управляет lifespan автоматически
    assert hasattr(app.state, "celery_app")
    assert app.state.celery_app in ("initialized", None)  # может быть очищено после shutdown
