import logging
from typing import List

import pytest
import requests

from data.mongo_schemas.user_notes.user_note import UserNote
from data.schemas.users.user import User
from test.integration_tests.utils.fake_user_note import generate_random_user_note_to_create
from test.utils.user_api import user_notes as user_notes_api

logger = logging.getLogger(__name__)

@pytest.fixture
def created_user_note(test_client_logged_in: requests.Session, logged_in_user: User) -> UserNote:
    user_note = generate_random_user_note_to_create(logged_in_user.id)
    return user_notes_api.create_user_note(test_client_logged_in, user_note)

@pytest.fixture
def created_n_user_notes(test_client_logged_in: requests.Session, logged_in_user: User, n_user_notes: int = 5) -> List[UserNote]:
    user_notes = []
    for _ in range(n_user_notes):
        user_note = generate_random_user_note_to_create(logged_in_user.id)
        user_notes.append(
            user_notes_api.create_user_note(test_client_logged_in, user_note)
        )
    return user_notes
