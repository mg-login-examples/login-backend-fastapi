import logging
from typing import List
import random
import string

import pytest
import requests

from admin.data.schemas.quotes.quoteCreate import QuoteCreate
from admin.data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from admin.data.schemas.users.userDeep import User as UserDeep
from test.integration_tests.fixtures.client import test_client
from test.integration_tests.fixtures.users import created_user


logger = logging.getLogger(__name__)

def generate_random_quote_to_create(user: UserDeep) -> QuoteCreate:
    quote_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    quote = QuoteCreate(text=quote_text, author=user)
    return quote

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
