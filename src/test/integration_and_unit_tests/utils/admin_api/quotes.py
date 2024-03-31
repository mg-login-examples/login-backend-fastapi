import requests  # type: ignore

from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.quotes.quoteCreate import QuoteCreate
from test.integration_and_unit_tests.integration_tests.utils import asserts


def get_quote(test_client: requests.Session, quote_id: int) -> QuoteDeep:
    response = test_client.get(f"/api/admin/resource/quotes/{quote_id}/")
    assert response.status_code == 200
    return QuoteDeep(**response.json())


def create_quote(test_client: requests.Session,
                 quote_to_create: QuoteCreate) -> QuoteDeep:
    response = test_client.post(
        "/api/admin/resource/quotes/", json=quote_to_create.model_dump())
    assert response.status_code == 200
    return QuoteDeep(**response.json())


def put_quote(test_client: requests.Session, quote_to_edit: QuoteDeep):
    response = test_client.put(
        f"/api/admin/resource/quotes/{quote_to_edit.id}/", json=quote_to_edit.model_dump())
    assert response.status_code == 204


def delete_quote(test_client: requests.Session, quote_id: int):
    response = test_client.delete(f"/api/admin/resource/quotes/{quote_id}/")
    assert response.status_code == 204


def get_quotes(test_client: requests.Session, skip=0,
               limit=10) -> list[QuoteDeep]:
    response = test_client.get(
        f"/api/admin/resource/quotes/?skip={skip}&limit={limit}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    quotes = [QuoteDeep(**quote_json) for quote_json in response.json()]
    return quotes


def get_quote_expect_not_found(test_client: requests.Session, quote_id: int):
    response = test_client.get(f"/api/admin/resource/quotes/{quote_id}/")
    assert response.status_code == 404
    asserts.assert_response_error_item_not_found(response)
