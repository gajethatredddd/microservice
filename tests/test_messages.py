import pytest
from fastapi.testclient import TestClient
from app.main import create_app

app = create_app()
client = TestClient(app)

def test_send_message_success(monkeypatch):
    def fake_delay(to_email, image_id):
        return True
    from app.tasks.celery_tasks import send_email_task
    monkeypatch.setattr(send_email_task, "delay", fake_delay)

    response = client.post("/api/send_message_to_email", json={
        "to_email": "test@example.com",
        "image_id": "123"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
