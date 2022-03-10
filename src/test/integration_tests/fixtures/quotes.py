import logging
from typing import List
import random
import string

import pytest
import requests

from data.schemas.quotes.quoteCreate import QuoteCreate
from data.schemas.quotes.quote import Quote
from data.schemas.users.user import User
from test.integration_tests.fixtures.client import test_client
from test.integration_tests.fixtures.users import created_user


logger = logging.getLogger(__name__)

def generate_random_quote_to_create(user: User) -> QuoteCreate:
    quote_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    quote = QuoteCreate(text=quote_text, author=user)
    return quote

@pytest.fixture
def created_quote(test_client: requests.Session, created_user: User) -> Quote:
    quote = generate_random_quote_to_create(created_user)
    response = test_client.post("/api/quotes/", json=quote.dict())
    assert response.status_code == 200
    return Quote(**response.json())

@pytest.fixture
def created_n_quotes(test_client: requests.Session, created_user: User, n_quotes: int = 5) -> List[Quote]:
    quotes = []
    for _ in range(n_quotes):
        quote = generate_random_quote_to_create(created_user)
        response = test_client.post("/api/quotes/", json=quote.dict())
        assert response.status_code == 200
        quotes.append(
            Quote(**response.json())
        )
    return quotes
