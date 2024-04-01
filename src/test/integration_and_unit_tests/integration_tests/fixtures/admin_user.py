import pytest
import requests  # type: ignore
import logging

from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.admin_users.admin_user import AdminUser
from data.schemas.admin_users.admin_user_create import AdminUserCreate
from test.integration_and_unit_tests.utils.admin_api import (
    authentication as admin_authentication_api,
)
from test.env_settings_test import EnvSettingsTest

logger = logging.getLogger(__name__)


@pytest.fixture
def admin_user_login(env_settings_test: EnvSettingsTest) -> AdminUserCreate:
    logger.debug("Create fixture admin_user_login")
    return AdminUserCreate(
        email=env_settings_test.admin_user_email,
        password=env_settings_test.admin_user_password,
    )


@pytest.fixture
def admin_login_response(
    test_client: requests.Session, admin_user_login: AdminUserCreate
) -> AdminLoginResponse:
    logger.debug("Create fixture admin_login_response")
    return admin_authentication_api.login(test_client, admin_user_login)


@pytest.fixture
def logged_in_admin_user(test_client_admin_logged_in: requests.Session) -> AdminUser:
    logger.debug("Create fixture logged_in_admin_user")
    admin_authentication_api.authenticate(test_client_admin_logged_in)
    return test_client_admin_logged_in
