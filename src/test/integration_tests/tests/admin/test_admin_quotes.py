import logging
from typing import List

import requests
import pytest

from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.users.userDeep import User as UserDeep
from data.schemas.users.user import User
from test.integration_tests.fixtures.client import test_client
from test.integration_tests.fixtures.quotes_admin import created_quote_by_admin, created_n_quotes_by_admin, generate_random_quote_to_create
from test.integration_tests.fixtures.users_admin import created_user_by_admin, created_n_users_by_admin
from test.integration_tests.fixtures.dbutils import setup_db
from test.integration_tests.utils import asserts

logger = logging.getLogger(__name__)

# Test that a quote can be fetched by id
def test_get_quote(test_client: requests.Session, created_quote_by_admin: QuoteDeep):
    response = test_client.get(f"/api/admin/resource/quotes/{created_quote_by_admin.id}/")
    assert response.status_code == 200
    quote = QuoteDeep(**response.json())
    assert quote.id == created_quote_by_admin.id
    assert quote == created_quote_by_admin

# Test that a quote can be created
def test_create_quote(test_client: requests.Session, created_user_by_admin: User):
    quote = generate_random_quote_to_create(created_user_by_admin)
    response = test_client.post("/api/admin/resource/quotes/", json=quote.dict())
    assert response.status_code == 200
    created_quote = QuoteDeep(**response.json())
    assert created_quote.text == quote.text
    assert created_quote.author.id == quote.author.id
    assert created_quote.id is not None

# Test that multiple quotes can be fetched
@pytest.mark.parametrize("created_n_quotes_by_admin", [5], indirect=True)
def test_get_quotes(test_client: requests.Session, created_n_quotes_by_admin: List[QuoteDeep]):
    response = test_client.get(f"/api/admin/resource/quotes/?skip=0&limit=4")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    quotes = [QuoteDeep(**quote_json) for quote_json in response.json()]
    assert len(quotes) == 4
    for quote in quotes:
        assert quote.id is not None

# Test that a quote can be updated
@pytest.mark.parametrize("created_n_users_by_admin", [1], indirect=True)
def test_put_quote(test_client: requests.Session, created_n_users_by_admin: List[UserDeep], created_quote_by_admin: QuoteDeep):
    new_text = "new text"
    assert created_quote_by_admin.text != new_text
    created_quote_by_admin.text = new_text
    assert created_quote_by_admin.author.id != created_n_users_by_admin[0].id
    created_quote_by_admin.author = created_n_users_by_admin[0]
    response = test_client.put(f"/api/admin/resource/quotes/{created_quote_by_admin.id}/", json=created_quote_by_admin.dict())
    assert response.status_code == 204
    response = test_client.get(f"/api/admin/resource/quotes/{created_quote_by_admin.id}/")
    assert response.status_code == 200
    quote = QuoteDeep(**response.json())
    assert quote.text == new_text
    assert quote.author.id == created_n_users_by_admin[0].id

# Test that a quote can be deleted by id
def test_delete_quote(test_client: requests.Session, created_quote_by_admin: QuoteDeep):
    response = test_client.delete(f"/api/admin/resource/quotes/{created_quote_by_admin.id}/")
    assert response.status_code == 204
    response = test_client.get(f"/api/admin/resource/quotes/{created_quote_by_admin.id}/")
    assert response.status_code == 404
    asserts.assert_response_error_item_not_found(response)
