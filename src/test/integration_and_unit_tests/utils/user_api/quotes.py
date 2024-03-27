import requests

from data.schemas.quotes.quote import Quote
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.quotes.quoteCreate import QuoteCreate


def create_quote(test_client: requests.Session,
                 quote_to_create: QuoteCreate) -> QuoteDeep:
    response = test_client.post(
        "/api/quotes/", json=quote_to_create.model_dump())
    assert response.status_code == 200
    return QuoteDeep(**response.json())


def edit_quote(test_client: requests.Session, quote_to_edit: Quote):
    response = test_client.put(
        f"/api/quotes/{quote_to_edit.id}/", json=quote_to_edit.model_dump())
    assert response.status_code == 204


def delete_quote(test_client: requests.Session, quote_id: int):
    response = test_client.delete(f"/api/quotes/{quote_id}/")
    assert response.status_code == 204


def get_quotes(test_client: requests.Session, skip=0,
               limit=10) -> list[QuoteDeep]:
    response = test_client.get(f"/api/quotes/?skip={skip}&limit={limit}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    quotes = [QuoteDeep(**quote_json) for quote_json in response.json()]
    return quotes


def get_user_quotes(test_client: requests.Session,
                    user_id: int, skip=0, limit=10) -> list[QuoteDeep]:
    response = test_client.get(
        f"/api/users/{user_id}/quotes/?skip={skip}&limit={limit}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    quotes = [QuoteDeep(**quote_json) for quote_json in response.json()]
    return quotes


def like_quote(test_client: requests.Session, quote_id: int, user_id: int):
    response = test_client.put(f"/api/quotes/{quote_id}/users/{user_id}/like/")
    assert response.status_code == 204


def unlike_quote(test_client: requests.Session, quote_id: int, user_id: int):
    response = test_client.delete(
        f"/api/quotes/{quote_id}/users/{user_id}/like/")
    assert response.status_code == 204
