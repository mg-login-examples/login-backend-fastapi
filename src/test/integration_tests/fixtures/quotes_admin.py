import logging
from typing import List
import random
import string

import pytest
import requests

from data.schemas.quotes.quoteCreate import QuoteCreate
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.users.userDeep import User as UserDeep
from test.integration_tests.fixtures.client import test_client
from test.integration_tests.fixtures.users import created_user
from test.integration_tests.utils.fake_quote import generate_random_quote_to_create

logger = logging.getLogger(__name__)

@pytest.fixture
def created_quote_by_admin(test_client: requests.Session, created_user_by_admin: UserDeep) -> QuoteDeep:
    quote = generate_random_quote_to_create(created_user_by_admin)
    response = test_client.post("/api/admin/resource/quotes/", json=quote.dict())
    assert response.status_code == 200
    return QuoteDeep(**response.json())

@pytest.fixture
def created_n_quotes_by_admin(test_client: requests.Session, created_user_by_admin: UserDeep, n_quotes: int = 5) -> List[QuoteDeep]:
    quotes = []
    for _ in range(n_quotes):
        quote = generate_random_quote_to_create(created_user_by_admin)
        response = test_client.post("/api/admin/resource/quotes/", json=quote.dict())
        assert response.status_code == 200
        quotes.append(
            QuoteDeep(**response.json())
        )
    return quotes
