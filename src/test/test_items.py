from fastapi.testclient import TestClient
import logging
from main import app


logger = logging.getLogger(__name__)

client = TestClient(app)

def test_get_items_for_all():
    response = client.get("/api/items/for-all")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "item 1"}, {"id": 2, "name": "item 2"}]

def test_get_items_for_logged_in():
    response = client.get("/api/items/for-logged-in")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "private item 1"}, {"id": 2, "name": "private item 2"}]
