import logging
from typing import List

import requests

from test.integration_tests.fixtures.client import test_client
from test.integration_tests.fixtures.items import created_item, created_5_items, generate_random_item_to_create
from test.integration_tests.fixtures.dbutils import setup_db
from data.schemas.items import Item

logger = logging.getLogger(__name__)

def test_get_item(test_client: requests.Session, created_item: Item):
    response = test_client.get(f"/api/items/{created_item.id}/")
    item = Item(**response.json())
    assert response.status_code == 200
    assert item.id == created_item.id

def test_get_items(test_client: requests.Session, created_5_items: List[Item]):
    response = test_client.get(f"/api/items/")
    assert response.status_code == 200
    assert len(response.json()) >= 5

def test_create_item(test_client: requests.Session):
    item = generate_random_item_to_create()
    response = test_client.post("/api/items/", json=item.dict())
    assert response.status_code == 200
    created_item = Item(**response.json())
    assert created_item.name == item.name
    assert created_item.description == item.description

def test_delete_item(test_client: requests.Session, created_item: Item):
    response = test_client.delete(f"/api/items/{created_item.id}/")
    assert response.status_code == 204
