import logging
from test.integration_and_unit_tests.integration_tests.utils.fake_quote import \
    generate_random_quote_to_create
from test.integration_and_unit_tests.utils.user_api import quotes as quotes_api

import pytest
import requests  # type: ignore

from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.users.user import User

logger = logging.getLogger(__name__)


@pytest.fixture
def created_quote(
    test_client_logged_in: requests.Session, logged_in_user: User
) -> QuoteDeep:
    logger.debug("Create fixture created_quote")
    quote = generate_random_quote_to_create(logged_in_user)
    return quotes_api.create_quote(test_client_logged_in, quote)


@pytest.fixture
def created_n_quotes(
    test_client_logged_in: requests.Session, logged_in_user: User, n_quotes: int = 5
) -> list[QuoteDeep]:
    logger.debug("Create fixture created_n_quotes")
    quotes = []
    for _ in range(n_quotes):
        quote = generate_random_quote_to_create(logged_in_user)
        quotes.append(quotes_api.create_quote(test_client_logged_in, quote))
    return quotes
