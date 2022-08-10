
import logging
from typing import List

import requests
import pytest

from data.schemas.users.user import User
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from test.integration_tests.utils.fake_quote import generate_random_quote_to_create
from test.utils.api import quotes as quotes_api
from test.utils.admin_api import quotes as quotes_admin_api

logger = logging.getLogger(__name__)

# Test that a quote can be created
def test_create_quote(test_client_logged_in: requests.Session, logged_in_user: User):
    quote = generate_random_quote_to_create(logged_in_user)
    created_quote = quotes_api.create_quote(test_client_logged_in, quote)
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
def test_get_user_quotes(test_client_logged_in: requests.Session, logged_in_user: User, created_n_quotes: List[QuoteDeep]):
    quotes = quotes_api.get_user_quotes(test_client_logged_in, logged_in_user.id, limit=4)
    assert len(quotes) == 4
    for quote in quotes:
        assert quote.id is not None
        assert quote.author.id == logged_in_user.id

# Test that a quote's text can be edit
def test_edit_quote(test_client_logged_in: requests.Session, created_quote: QuoteDeep):
    assert created_quote.text != "quote text changed"
    created_quote.text = "quote text changed"
    quotes_api.edit_quote(test_client_logged_in, created_quote)
    edited_quote = quotes_admin_api.get_quote(test_client_logged_in, created_quote.id)
    assert edited_quote.text == "quote text changed"

# Test that when calling endpoint to edit a quote's text, changes in other fields are ignored
def test_edit_quote_ignore_other_changes(test_client_logged_in: requests.Session, created_quote: QuoteDeep):
    # Edit quote text
    created_quote.text = "quote text changed"
    # Edit quote author id
    actual_author_id = created_quote.author.id
    created_quote.author.id += 1
    # Edit quote liked by users field
    actual_liked_by_users = created_quote.liked_by_users
    created_quote.liked_by_users = [created_quote.author]
    # Call edit quote endpoint
    quotes_api.edit_quote(test_client_logged_in, created_quote)
    # Get quote by id
    edited_quote = quotes_admin_api.get_quote(test_client_logged_in, created_quote.id)
    # Assert quote text updated
    assert edited_quote.text == "quote text changed"
    # Assert other edited fields not changed
    assert edited_quote.author.id == actual_author_id
    assert edited_quote.author.id != created_quote.author.id
    assert edited_quote.liked_by_users == actual_liked_by_users
    assert edited_quote.liked_by_users != created_quote.liked_by_users

# Test that a quote can be deleted by id
def test_delete_quote(test_client_logged_in: requests.Session, created_quote: QuoteDeep):
    quotes_api.delete_quote(test_client_logged_in, created_quote.id)
    quotes_admin_api.get_quote_expect_not_found(test_client_logged_in, created_quote.id)

# Test that a quote can be liked
def test_like_quote(test_client_logged_in: requests.Session, logged_in_user: User, created_quote_by_admin: QuoteDeep):
    quotes_api.like_quote(test_client_logged_in, created_quote_by_admin.id, logged_in_user.id)
    quote = quotes_admin_api.get_quote(test_client_logged_in, created_quote_by_admin.id)
    all_liked_user_ids = [user.id for user in quote.liked_by_users]
    assert logged_in_user.id in all_liked_user_ids

# Test that a quote can be unliked
def test_unlike_quote(test_client_logged_in: requests.Session, logged_in_user: User, created_quote_by_admin: QuoteDeep):
    quotes_api.like_quote(test_client_logged_in, created_quote_by_admin.id, logged_in_user.id)
    quotes_api.unlike_quote(test_client_logged_in, created_quote_by_admin.id, logged_in_user.id)
    quote = quotes_admin_api.get_quote(test_client_logged_in, created_quote_by_admin.id)
    all_liked_user_ids = [user.id for user in quote.liked_by_users]
    assert logged_in_user.id not in all_liked_user_ids
