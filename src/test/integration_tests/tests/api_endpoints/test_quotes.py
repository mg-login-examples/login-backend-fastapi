
import logging
from typing import List

import requests
import pytest

from data.schemas.users.user import User
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from test.integration_tests.utils.fake_quote import generate_random_quote_to_create
from test.utils.api import quotes as quotes_api

logger = logging.getLogger(__name__)

# Test that a quote can be created
def test_create_quote(test_client: requests.Session, created_user: User):
    quote = generate_random_quote_to_create(created_user)
    created_quote = quotes_api.create_quote(test_client, quote)
    assert created_quote.text == quote.text
    assert created_quote.author.id == quote.author.id
    assert created_quote.id is not None
    assert isinstance(created_quote.liked_by_users, List)

# Test that multiple quotes can be fetched
@pytest.mark.parametrize("created_n_quotes", [5], indirect=True)
def test_get_quotes(test_client: requests.Session, created_n_quotes: List[QuoteDeep]):
    quotes = quotes_api.get_quotes(test_client, limit=4)
    assert len(quotes) == 4
    for quote in quotes:
        assert quote.id is not None

# Test that multiple user quotes can be fetched
@pytest.mark.parametrize("created_n_quotes", [5], indirect=True)
def test_get_user_quotes(test_client: requests.Session, created_user: User, created_n_quotes: List[QuoteDeep]):
    quotes = quotes_api.get_user_quotes(test_client, created_user.id, limit=4)
    assert len(quotes) == 4
    for quote in quotes:
        assert quote.id is not None
        assert quote.author.id == created_user.id

# Test that a quote can be deleted by id
def test_delete_quote(test_client: requests.Session, created_quote: QuoteDeep):
    quotes_api.delete_quote(test_client, created_quote.id)
