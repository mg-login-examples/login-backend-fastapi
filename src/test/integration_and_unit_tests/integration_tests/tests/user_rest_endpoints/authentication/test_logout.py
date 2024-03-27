import logging

import requests

logger = logging.getLogger(__name__)


def test_logout(test_client_logged_in: requests.Session):
    response = test_client_logged_in.post("/api/logout/")
    assert response.status_code == 200
    assert response.cookies.get("Authorization") is None
    assert test_client_logged_in.cookies.get("Authorization") is None
    response = test_client_logged_in.post("/api/authenticate/")
    assert response.status_code == 403
