
import logging
from typing import List

import requests
import pytest

from data.schemas.users.user import User
from data.schemas.quotes.quote import Quote
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from test.integration_tests.fixtures.client import test_client
from test.integration_tests.fixtures.users import created_user
from test.integration_tests.fixtures.quotes import created_quote, created_n_quotes, generate_random_quote_to_create
from test.integration_tests.fixtures.dbutils import setup_db
from test.integration_tests.utils import asserts

logger = logging.getLogger(__name__)

# Test that a quote can be created
def test_create_quote(test_client: requests.Session, created_user: User):
    quote = generate_random_quote_to_create(created_user)
    response = test_client.post("/api/quotes/", json=quote.dict())
    assert response.status_code == 200
    created_quote = QuoteDeep(**response.json())
    assert created_quote.text == quote.text
    assert created_quote.author.id == quote.author.id
    assert created_quote.id is not None
    assert isinstance(created_quote.liked_by_users, List)

# Test that multiple quotes can be fetched
@pytest.mark.parametrize("created_n_quotes", [5], indirect=True)
def test_get_quotes(test_client: requests.Session, created_n_quotes: List[QuoteDeep]):
    response = test_client.get("/api/quotes/?skip=0&limit=4")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    quotes = [QuoteDeep(**quote_json) for quote_json in response.json()]
    assert len(quotes) == 4
    for quote in quotes:
        assert quote.id is not None

# Test that multiple user quotes can be fetched
@pytest.mark.parametrize("created_n_quotes", [5], indirect=True)
def test_get_user_quotes(test_client: requests.Session, created_user: User, created_n_quotes: List[QuoteDeep]):
    response = test_client.get(f"/api/users/{created_user.id}/quotes/?skip=0&limit=4")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    quotes = [QuoteDeep(**quote_json) for quote_json in response.json()]
    assert len(quotes) == 4
    for quote in quotes:
        assert quote.id is not None
        assert quote.author.id == created_user.id

# Test that a quote can be deleted by id
def test_delete_quote(test_client: requests.Session, created_quote: QuoteDeep):
    response = test_client.delete(f"/api/quotes/{created_quote.id}/")
    assert response.status_code == 204
