import logging
from typing import List

import requests
import pytest
from mimesis import Text

from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.users.userDeep import User as UserDeep
from data.schemas.users.user import User
from test.integration_tests.utils.fake_quote import generate_random_quote_to_create
from test.utils.admin_api import quotes as quotes_admin_api

logger = logging.getLogger(__name__)

text = Text('en')

# Test that a quote can be fetched by id
def test_get_quote(test_client: requests.Session, created_quote_by_admin: QuoteDeep):
    quote = quotes_admin_api.get_quote(test_client, created_quote_by_admin.id)
    assert quote.id == created_quote_by_admin.id
    assert quote == created_quote_by_admin

# Test that a quote can be created
def test_create_quote(test_client: requests.Session, created_user_by_admin: User):
    quote_to_create = generate_random_quote_to_create(created_user_by_admin)
    created_quote = quotes_admin_api.create_quote(test_client, quote_to_create)
    assert created_quote.text == quote_to_create.text
    assert created_quote.author.id == quote_to_create.author.id
    assert created_quote.id is not None

# Test that multiple quotes can be fetched
@pytest.mark.parametrize("created_n_quotes_by_admin", [5], indirect=True)
def test_get_quotes(test_client: requests.Session, created_n_quotes_by_admin: List[QuoteDeep]):
    quotes = quotes_admin_api.get_quotes(test_client, skip=0, limit=4)
    assert len(quotes) == 4
    for quote in quotes:
        assert quote.id is not None

# Test that a quote can be updated
@pytest.mark.parametrize("created_n_users_by_admin", [1], indirect=True)
def test_put_quote(test_client_admin_logged_in: requests.Session, created_n_users_by_admin: List[UserDeep], created_quote_by_admin: QuoteDeep):
    new_text = text.quote()
    assert created_quote_by_admin.text != new_text
    created_quote_by_admin.text = new_text
    assert created_quote_by_admin.author.id != created_n_users_by_admin[0].id
    created_quote_by_admin.author = created_n_users_by_admin[0]
    quotes_admin_api.put_quote(test_client_admin_logged_in, created_quote_by_admin)
    quote = quotes_admin_api.get_quote(test_client_admin_logged_in, created_quote_by_admin.id)
    assert quote.text == new_text
    assert quote.author.id == created_n_users_by_admin[0].id

# Test that a quote can be deleted by id
def test_delete_quote(test_client_admin_logged_in: requests.Session, created_quote_by_admin: QuoteDeep):
    quotes_admin_api.delete_quote(test_client_admin_logged_in, created_quote_by_admin.id)
    quotes_admin_api.get_quote_expect_not_found(test_client_admin_logged_in, created_quote_by_admin.id)
