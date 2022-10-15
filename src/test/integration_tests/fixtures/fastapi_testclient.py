
import pytest
import logging

import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient

from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.authentication.login_response import LoginResponse

logger = logging.getLogger(__name__)

@pytest.fixture
def test_client(app: FastAPI) -> requests.Session:
    return TestClient(app)

@pytest.fixture
def test_client_admin_logged_in(test_client: requests.Session, admin_login_response: AdminLoginResponse) -> requests.Session:
    return test_client

@pytest.fixture
def test_client_logged_in(test_client: requests.Session, login_response: LoginResponse) -> requests.Session:
    return test_client

@pytest.fixture
def test_client_after_app_start(test_client: requests.Session) -> requests.Session:
    with test_client as test_client:
        yield test_client
