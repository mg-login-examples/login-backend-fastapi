import logging
from typing import List

import pytest
import requests

from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.users.userDeep import User as UserDeep
from test.integration_tests.utils.fake_quote import generate_random_quote_to_create
from test.utils.admin_api import quotes as quotes_admin_api

logger = logging.getLogger(__name__)

@pytest.fixture
def created_quote_by_admin(test_client_admin_logged_in: requests.Session, created_user_by_admin: UserDeep) -> QuoteDeep:
    logger.debug("Create fixture created_quote_by_admin")
    quote = generate_random_quote_to_create(created_user_by_admin)
    return quotes_admin_api.create_quote(test_client_admin_logged_in, quote)

@pytest.fixture
def created_n_quotes_by_admin(test_client_admin_logged_in: requests.Session, created_user_by_admin: UserDeep, n_quotes: int = 5) -> List[QuoteDeep]:
    logger.debug("Create fixture created_n_quotes_by_admin")
    quotes = []
    for _ in range(n_quotes):
        quote = generate_random_quote_to_create(created_user_by_admin)
        quotes.append(
            quotes_admin_api.create_quote(test_client_admin_logged_in, quote)
        )
    return quotes
