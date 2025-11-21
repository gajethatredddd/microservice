from fastapi.testclient import TestClient
from app.main import create_app
from app.core.di import get_message_service
from app.services.message_service import MessageService

def test_get_message_service_instance():
    svc = get_message_service()
    assert isinstance(svc, MessageService)

def test_send_message_endpoint(monkeypatch):
    app = create_app()
    client = TestClient(app)

    # Подменим delay метода celery task
    def fake_delay(to_email, image_id):
        return True

    from app.tasks.celery_tasks import send_email_task
    monkeypatch.setattr(send_email_task, "delay", fake_delay)

    resp = client.post("/api/send_message_to_email", json={
        "to_email": "tt@example.com",
        "image_id": "abc"
    })

    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
