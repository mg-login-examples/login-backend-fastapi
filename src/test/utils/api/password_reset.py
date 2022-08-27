import requests

from data.schemas.users.user import User
from test.integration_tests.utils import asserts

import logging
logger = logging.getLogger(__name__)

def generate_password_reset_link(test_client: requests.Session, email: str) -> User:
    payload = { "email" : email }
    response = test_client.post(f"/api/password-reset-link/", json=payload)
    assert response.status_code == 204

def reset_password(test_client: requests.Session, email: str, password: str, token: str):
    payload = {
        "email": email,
        "password": password,
        "token": token
    }
    response = test_client.post("/api/password-reset/", json=payload)
    assert response.status_code == 204

def reset_password_expect_unauthorized(test_client: requests.Session, email: str, password: str, token: str):
    payload = {
        "email": email,
        "password": password,
        "token": token
    }
    response = test_client.post("/api/password-reset/", json=payload)
    assert response.status_code == 401
    asserts.assert_response_error_invalid_link(response)
