from fastapi.testclient import TestClient
from app.main import create_app
from app.core.exceptions import CustomException

app = create_app()
client = TestClient(app)

def test_custom_exception_handling():
    # временно добавим маршрут, который поднимет CustomException
    @app.get("/raise_custom")
    async def raise_custom():
        raise CustomException("boom", status_code=418)

    resp = client.get("/raise_custom")
    assert resp.status_code == 418
    data = resp.json()
    assert "detail" in data or "message" in data
