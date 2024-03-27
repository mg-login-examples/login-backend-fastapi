import logging

import pytest
import requests

from data.mongo_schemas.user_notes.user_note import UserNote
from data.schemas.users.userDeep import User as UserDeep
from test.integration_and_unit_tests.integration_tests.utils.fake_user_note import generate_random_user_note_to_create
from test.integration_and_unit_tests.utils.admin_api import user_notes as user_notes_admin_api

logger = logging.getLogger(__name__)


@pytest.fixture
def created_user_note_by_admin(
        test_client_admin_logged_in: requests.Session, created_user_by_admin: UserDeep) -> UserNote:
    logger.debug("Create fixture created_user_note_by_admin")
    user_note = generate_random_user_note_to_create(created_user_by_admin.id)
    return user_notes_admin_api.create_user_note(
        test_client_admin_logged_in, user_note)


@pytest.fixture
def created_n_user_notes_by_admin(test_client_admin_logged_in: requests.Session,
                                  created_user_by_admin: UserDeep, n_user_notes: int = 5) -> list[UserNote]:
    logger.debug("Create fixture created_n_user_notes_by_admin")
    user_notes = []
    for _ in range(n_user_notes):
        user_note = generate_random_user_note_to_create(
            created_user_by_admin.id)
        user_notes.append(
            user_notes_admin_api.create_user_note(
                test_client_admin_logged_in, user_note)
        )
    return user_notes
