import logging

import requests  # type: ignore
import pytest
from mimesis import Text

from data.mongo_schemas.user_notes.user_note import UserNote
from data.schemas.users.userDeep import User as UserDeep
from data.schemas.users.user import User
from test.integration_and_unit_tests.integration_tests.utils.fake_user_note import generate_random_user_note_to_create
from test.integration_and_unit_tests.utils.admin_api import user_notes as user_notes_admin_api

logger = logging.getLogger(__name__)

text = Text('en')

# Test that a user note can be fetched by id


def test_get_user_note(test_client: requests.Session,
                       created_user_note_by_admin: UserNote):
    user_note = user_notes_admin_api.get_user_note(
        test_client, str(created_user_note_by_admin.id))
    assert user_note.id == created_user_note_by_admin.id
    assert user_note == created_user_note_by_admin

# Test that a user note can be created


def test_create_user_note(test_client: requests.Session,
                          created_user_by_admin: User):
    user_note_to_create = generate_random_user_note_to_create(
        created_user_by_admin.id)
    created_user_note = user_notes_admin_api.create_user_note(
        test_client, user_note_to_create)
    assert created_user_note.text == user_note_to_create.text
    assert created_user_note.user_id == user_note_to_create.user_id
    assert created_user_note.id is not None

# Test that multiple user notes can be fetched


@pytest.mark.parametrize("created_n_user_notes_by_admin", [5], indirect=True)
def test_get_user_notes(test_client: requests.Session,
                        created_n_user_notes_by_admin: list[UserNote]):
    user_notes = user_notes_admin_api.get_user_notes(
        test_client, skip=0, limit=4)
    assert len(user_notes) == 4
    for user_note in user_notes:
        assert user_note.id is not None

# Test that a user note can be updated


@pytest.mark.parametrize("created_n_users_by_admin", [1], indirect=True)
def test_put_user_note(test_client_admin_logged_in: requests.Session,
                       created_n_users_by_admin: list[UserDeep], created_user_note_by_admin: UserNote):
    new_text = text.sentence()
    assert created_user_note_by_admin.text != new_text
    created_user_note_by_admin.text = new_text
    new_title = text.title()
    assert created_user_note_by_admin.title != new_title
    created_user_note_by_admin.title = new_title
    assert created_user_note_by_admin.user_id != created_n_users_by_admin[0].id
    created_user_note_by_admin.user_id = created_n_users_by_admin[0].id
    user_notes_admin_api.put_user_note(
        test_client_admin_logged_in, created_user_note_by_admin)
    user_note = user_notes_admin_api.get_user_note(
        test_client_admin_logged_in, str(created_user_note_by_admin.id))
    assert user_note.text == new_text
    assert str(user_note.user_id) == str(created_n_users_by_admin[0].id)

# Test that a user note can be deleted by id


def test_delete_user_note(
        test_client_admin_logged_in: requests.Session, created_user_note_by_admin: UserNote):
    user_notes_admin_api.delete_user_note(
        test_client_admin_logged_in, str(created_user_note_by_admin.id))
    user_notes_admin_api.get_user_note_expect_not_found(
        test_client_admin_logged_in, str(created_user_note_by_admin.id))
