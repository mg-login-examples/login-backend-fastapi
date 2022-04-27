import logging
from typing import List

import pytest
import requests

from data.schemas.quotes.quote import Quote
from data.schemas.users.user import User
from test.integration_tests.utils.fake_quote import generate_random_quote_to_create
from test.utils.api import quotes as quotes_api

logger = logging.getLogger(__name__)

@pytest.fixture
def created_quote(test_client: requests.Session, created_user: User) -> Quote:
    quote = generate_random_quote_to_create(created_user)
    return quotes_api.create_quote(test_client, quote)

@pytest.fixture
def created_n_quotes(test_client: requests.Session, created_user: User, n_quotes: int = 5) -> List[Quote]:
    quotes = []
    for _ in range(n_quotes):
        quote = generate_random_quote_to_create(created_user)
        quotes.append(
            quotes_api.create_quote(test_client, quote)
        )
    return quotes
