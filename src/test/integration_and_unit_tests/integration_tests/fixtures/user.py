import logging
from test.integration_and_unit_tests.integration_tests.utils.fake_user import (
    generate_random_user_to_create,
)
from test.integration_and_unit_tests.utils.admin_api import users as users_admin_api
from test.integration_and_unit_tests.utils.user_api import (
    authentication as authentication_api,
)

import pytest
import requests  # type: ignore

from data.schemas.authentication.login_response import LoginResponse
from data.schemas.users.user import User
from data.schemas.users.userCreate import UserCreate
from data.schemas.users.userDeep import User as UserDeep

logger = logging.getLogger(__name__)


@pytest.fixture
def user_login() -> UserCreate:
    logger.debug("Create fixture user_login")
    return generate_random_user_to_create()


@pytest.fixture
def created_unverified_user_by_admin(
    test_client_admin_logged_in: requests.Session, user_login: UserCreate
) -> UserDeep:
    logger.debug("Create fixture created_unverified_user_by_admin")
    return users_admin_api.create_user(test_client_admin_logged_in, user_login)


@pytest.fixture
def created_user_by_admin(
    test_client_admin_logged_in: requests.Session,
    created_unverified_user_by_admin: UserDeep,
) -> UserDeep:
    logger.debug("Create fixture created_user_by_admin")
    created_unverified_user_by_admin.is_verified = True
    users_admin_api.put_user(
        test_client_admin_logged_in, created_unverified_user_by_admin
    )
    return created_unverified_user_by_admin


@pytest.fixture
def login_response(
    test_client: requests.Session, user_login: UserCreate, created_user_by_admin: User
) -> LoginResponse:
    logger.debug("Create fixture login_response")
    return authentication_api.login(test_client, user_login)


@pytest.fixture
def logged_in_unverified_user(
    test_client: requests.Session,
    user_login: UserCreate,
    created_unverified_user_by_admin: User,
) -> User:
    logger.debug("Create fixture logged_in_unverified_user")
    login_response = authentication_api.login(test_client, user_login)
    return login_response.user


@pytest.fixture
def logged_in_user(login_response: LoginResponse) -> User:
    logger.debug("Create fixture logged_in_user")
    return login_response.user


@pytest.fixture
def created_n_users_by_admin(
    test_client_admin_logged_in: requests.Session, n_users: int = 5
) -> list[UserDeep]:
    logger.debug("Create fixture created_n_users_by_admin")
    users = []
    for _ in range(n_users):
        user = generate_random_user_to_create()
        users.append(users_admin_api.create_user(test_client_admin_logged_in, user))
    return users


@pytest.fixture
def user_2_login() -> UserCreate:
    logger.debug("Create fixture user_2_login")
    return generate_random_user_to_create()


@pytest.fixture
def created_user_2_by_admin(
    test_client_admin_logged_in: requests.Session, user_2_login: UserCreate
) -> UserDeep:
    logger.debug("Create fixture created_user_2_by_admin")
    user_2 = users_admin_api.create_user(test_client_admin_logged_in, user_2_login)
    user_2.is_verified = True
    users_admin_api.put_user(test_client_admin_logged_in, user_2)
    return user_2
