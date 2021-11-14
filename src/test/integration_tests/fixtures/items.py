import logging
from typing import List
import random
import string

import pytest
import requests

from test.integration_tests.fixtures.client import test_client
from data.schemas import items as itemSchemas

logger = logging.getLogger(__name__)

def generate_random_item_to_create():
    item_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    item_description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    item = itemSchemas.ItemCreate(name=item_name, description=item_description)
    return item

@pytest.fixture
def created_item(test_client: requests.Session) -> itemSchemas.Item:
    item = generate_random_item_to_create()
    response = test_client.post("/api/items/", json=item.dict())
    assert response.status_code == 200
    return itemSchemas.Item(**response.json())
    

@pytest.fixture
def created_5_items(test_client: requests.Session) -> List[itemSchemas.Item]:
    items = []
    for _ in range(5):
        item = generate_random_item_to_create()
        response = test_client.post("/api/items/", json=item.dict())
        assert response.status_code == 200
        items.append(
            itemSchemas.Item(**response.json())
        )
    return items
