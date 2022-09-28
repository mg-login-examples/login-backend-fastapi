
import logging
from typing import List

import requests
import pytest

from data.schemas.users.user import User
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from test.integration_tests.utils.fake_quote import generate_random_quote_to_create
from test.utils.user_api import quotes as quotes_api
from test.utils.admin_api import quotes as quotes_admin_api
from test.integration_tests.utils import asserts

logger = logging.getLogger(__name__)

# Test that a quote can be created for the logged in user
def test_create_quote(test_client_logged_in: requests.Session, logged_in_user: User):
    quote_to_create = generate_random_quote_to_create(logged_in_user)
    created_quote = quotes_api.create_quote(test_client_logged_in, quote_to_create)
    assert created_quote.text == quote_to_create.text
    assert created_quote.author.id == quote_to_create.author.id
    assert created_quote.id is not None
    assert isinstance(created_quote.liked_by_users, List)

# Test that a quote cannot be created for a user different than who is logged in
def test_create_quote_fails_when_quote_author_different_from_logged_in_user(
    test_client_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    quote_to_create = generate_random_quote_to_create(created_user_2_by_admin)
    response = test_client_logged_in.post("/api/quotes/", json=quote_to_create.dict())
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)

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

# Test that logged in user cannot get another user's quotes
@pytest.mark.parametrize("created_n_quotes", [5], indirect=True)
def test_get_user_quotes_fails_when_getting_quotes_of_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    logged_in_user: User, created_n_quotes: List[QuoteDeep],
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    response = test_client_logged_in.get(f"/api/users/{created_user_2_by_admin.id}/quotes/")
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)

# Test that a quote's text can be edit
def test_edit_quote_text(test_client_logged_in: requests.Session, created_quote: QuoteDeep):
    assert created_quote.text != "quote text changed"
    created_quote.text = "quote text changed"
    quotes_api.edit_quote(test_client_logged_in, created_quote)
    edited_quote = quotes_admin_api.get_quote(test_client_logged_in, created_quote.id)
    assert edited_quote.text == "quote text changed"

# Test that when calling endpoint to edit a quote's text, changes in other fields are ignored
def test_edit_quote_text_ignores_other_quote_field_changes(test_client_logged_in: requests.Session, created_quote: QuoteDeep):
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

# Test that another user's quote cannot be edited
def test_edit_quote_text_fails_when_updating_quote_of_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    test_client_admin_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    quote_by_user_2_to_create = generate_random_quote_to_create(created_user_2_by_admin)
    quote_by_user_2 = quotes_admin_api.create_quote(test_client_admin_logged_in, quote_by_user_2_to_create)
    assert quote_by_user_2.text != "quote text changed"
    quote_by_user_2.text = "quote text changed"
    response = test_client_logged_in.put(f"/api/quotes/{quote_by_user_2.id}/", json=quote_by_user_2.dict())
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)

# Test that a quote can be deleted by id
def test_delete_quote(test_client_logged_in: requests.Session, created_quote: QuoteDeep):
    quotes_api.delete_quote(test_client_logged_in, created_quote.id)
    quotes_admin_api.get_quote_expect_not_found(test_client_logged_in, created_quote.id)

# Test that another user's quote cannot be deleted
def test_delete_quote_fails_when_deleting_quote_of_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    test_client_admin_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    quote_by_user_2_to_create = generate_random_quote_to_create(created_user_2_by_admin)
    quote_by_user_2 = quotes_admin_api.create_quote(test_client_admin_logged_in, quote_by_user_2_to_create)
    response = test_client_logged_in.delete(f"/api/quotes/{quote_by_user_2.id}/")
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)

# Test that a quote can be liked
# This test tests the more common scenario of liking another user's quote
# though it is possible (no api restrictions) for a user to like their own quote
def test_like_quote(
    test_client_logged_in: requests.Session,
    test_client_admin_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    quote_by_user_2_to_create = generate_random_quote_to_create(created_user_2_by_admin)
    quote_by_user_2 = quotes_admin_api.create_quote(test_client_admin_logged_in, quote_by_user_2_to_create)
    assert quote_by_user_2.author.id != logged_in_user.id
    quotes_api.like_quote(test_client_logged_in, quote_by_user_2.id, logged_in_user.id)
    quote = quotes_admin_api.get_quote(test_client_logged_in, quote_by_user_2.id)
    all_liked_user_ids = [user.id for user in quote.liked_by_users]
    assert logged_in_user.id in all_liked_user_ids

# Test that a logged in user cannot like a quote as a different user
def test_like_quote_fails_when_quote_like_user_different_from_logged_in(
    test_client_logged_in: requests.Session,
    test_client_admin_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    quote_by_user_2_to_create = generate_random_quote_to_create(created_user_2_by_admin)
    quote_by_user_2 = quotes_admin_api.create_quote(test_client_admin_logged_in, quote_by_user_2_to_create)
    assert quote_by_user_2.author.id != logged_in_user.id
    response = test_client_logged_in.put(f"/api/quotes/{quote_by_user_2.id}/users/{created_user_2_by_admin.id}/like/")
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)

# Test that a quote can be unliked
def test_unlike_quote(
    test_client_logged_in: requests.Session,
    test_client_admin_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    quote_by_user_2_to_create = generate_random_quote_to_create(created_user_2_by_admin)
    quote_by_user_2 = quotes_admin_api.create_quote(test_client_admin_logged_in, quote_by_user_2_to_create)
    assert quote_by_user_2.author.id != logged_in_user.id
    quotes_api.like_quote(test_client_logged_in, quote_by_user_2.id, logged_in_user.id)
    quotes_api.unlike_quote(test_client_logged_in, quote_by_user_2.id, logged_in_user.id)
    quote = quotes_admin_api.get_quote(test_client_logged_in, quote_by_user_2.id)
    all_liked_user_ids = [user.id for user in quote.liked_by_users]
    assert logged_in_user.id not in all_liked_user_ids

# Test that a logged in user cannot unlike a quote as a different user
def test_like_quote_fails_when_quote_like_user_different_from_logged_in(
    test_client_logged_in: requests.Session,
    test_client_admin_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    quote_by_user_2_to_create = generate_random_quote_to_create(created_user_2_by_admin)
    quote_by_user_2 = quotes_admin_api.create_quote(test_client_admin_logged_in, quote_by_user_2_to_create)
    quote_by_user_2.liked_by_users = [created_user_2_by_admin]
    quotes_admin_api.put_quote(test_client_admin_logged_in, quote_by_user_2)
    assert quote_by_user_2.author.id != logged_in_user.id
    response = test_client_logged_in.delete(f"/api/quotes/{quote_by_user_2.id}/users/{created_user_2_by_admin.id}/like/")
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)
    quote = quotes_admin_api.get_quote(test_client_logged_in, quote_by_user_2.id)
    all_liked_user_ids = [user.id for user in quote.liked_by_users]
    assert created_user_2_by_admin.id in all_liked_user_ids
