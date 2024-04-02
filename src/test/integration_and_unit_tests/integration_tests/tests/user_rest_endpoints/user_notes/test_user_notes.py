import logging
from test.integration_and_unit_tests.integration_tests.utils import asserts
from test.integration_and_unit_tests.integration_tests.utils.fake_user_note import (
    generate_random_user_note_to_create,
)
from test.integration_and_unit_tests.utils.admin_api import (
    user_notes as user_notes_admin_api,
)
from test.integration_and_unit_tests.utils.user_api import user_notes as user_notes_api

import pytest
import requests  # type: ignore
from fastapi.encoders import jsonable_encoder

from data.mongo_schemas.user_notes.user_note import UserNote
from data.schemas.users.user import User

logger = logging.getLogger(__name__)

# Test that a user note can be created for the logged in user


def test_create_user_note(
    test_client_logged_in: requests.Session, logged_in_user: User
):
    user_note_to_create = generate_random_user_note_to_create(logged_in_user.id)
    created_user_note = user_notes_api.create_user_note(
        test_client_logged_in, user_note_to_create
    )
    assert created_user_note.title == user_note_to_create.title
    assert created_user_note.text == user_note_to_create.text
    assert created_user_note.user_id == user_note_to_create.user_id
    assert created_user_note.id is not None


# Test that a user note cannot be created for a user different than who is
# logged in


def test_create_user_note_fails_when_user_note_user_different_from_logged_in_user(
    test_client_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User,
):
    assert logged_in_user.id != created_user_2_by_admin.id
    user_note_to_create = generate_random_user_note_to_create(
        created_user_2_by_admin.id
    )
    response = test_client_logged_in.post(
        "/api/user-notes/", json=user_note_to_create.model_dump()
    )
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)


# Test that multiple user notes can be fetched


@pytest.mark.parametrize("created_n_user_notes", [5], indirect=True)
def test_get_user_notes_of_user(
    test_client_logged_in: requests.Session,
    logged_in_user: User,
    created_n_user_notes: list[UserNote],
):
    user_notes = user_notes_api.get_user_user_notes(
        test_client_logged_in, logged_in_user.id, limit=4
    )
    assert len(user_notes) == 4
    for user_note in user_notes:
        assert user_note.id is not None
        assert user_note.user_id == logged_in_user.id


# Test that logged in user cannot get another user's user notes


@pytest.mark.parametrize("created_n_user_notes", [5], indirect=True)
def test_get_user_notes_of_user_fails_when_getting_user_notes_of_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    logged_in_user: User,
    created_n_user_notes: list[UserNote],
    created_user_2_by_admin: User,
):
    assert logged_in_user.id != created_user_2_by_admin.id
    response = test_client_logged_in.get(
        f"/api/users/{created_user_2_by_admin.id}/user-notes/"
    )
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)


# Test that a user note's title & text can be edited


def test_edit_user_note_title_and_text(
    test_client_logged_in: requests.Session, created_user_note: UserNote
):
    assert created_user_note.title != "note title changed"
    created_user_note.title = "note title changed"
    assert created_user_note.text != "note text changed"
    created_user_note.text = "note text changed"
    user_notes_api.edit_user_note(test_client_logged_in, created_user_note)
    edited_user_note = user_notes_api.get_user_note(
        test_client_logged_in, str(created_user_note.id)
    )
    assert edited_user_note.title == "note title changed"
    assert edited_user_note.text == "note text changed"


# Test that when calling endpoint to edit a user note's title and text,
# changes in other fields are ignored


def test_edit_user_note_title_and_text_ignores_other_user_notes_field_changes(
    test_client_logged_in: requests.Session, created_user_note: UserNote
):
    # Edit user note text
    created_user_note.text = "user note text changed"
    # Edit user note user_id
    actual_user_id = created_user_note.user_id
    created_user_note.user_id += 1
    # Call edit user note endpoint
    user_notes_api.edit_user_note(test_client_logged_in, created_user_note)
    # Get user note by id
    edited_user_note = user_notes_admin_api.get_user_note(
        test_client_logged_in, str(created_user_note.id)
    )
    # Assert user note text updated
    assert edited_user_note.text == "user note text changed"
    # Assert other edited fields not changed
    assert edited_user_note.user_id == actual_user_id
    assert edited_user_note.user_id != created_user_note.user_id


# Test that another user's user note cannot be edited


def test_edit_user_note_fails_when_updating_user_note_of_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    test_client_admin_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User,
):
    assert logged_in_user.id != created_user_2_by_admin.id
    user_note_by_user_2_to_create = generate_random_user_note_to_create(
        created_user_2_by_admin.id
    )
    user_note_by_user_2 = user_notes_admin_api.create_user_note(
        test_client_admin_logged_in, user_note_by_user_2_to_create
    )
    assert user_note_by_user_2.text != "user note text changed"
    user_note_by_user_2.text = "user note text changed"
    response = test_client_logged_in.put(
        f"/api/user-notes/{user_note_by_user_2.id}/",
        json=jsonable_encoder(user_note_by_user_2),
    )
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)


# Test that a user note can be deleted by id


def test_delete_user_note(
    test_client_logged_in: requests.Session, created_user_note: UserNote
):
    user_notes_api.delete_user_note(test_client_logged_in, str(created_user_note.id))
    user_notes_admin_api.get_user_note_expect_not_found(
        test_client_logged_in, str(created_user_note.id)
    )


# Test that another user's user note cannot be deleted


def test_delete_user_note_fails_when_deleting_user_note_of_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    test_client_admin_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User,
):
    assert logged_in_user.id != created_user_2_by_admin.id
    user_note_by_user_2_to_create = generate_random_user_note_to_create(
        created_user_2_by_admin.id
    )
    user_note_by_user_2 = user_notes_admin_api.create_user_note(
        test_client_admin_logged_in, user_note_by_user_2_to_create
    )
    response = test_client_logged_in.delete(
        f"/api/user-notes/{user_note_by_user_2.id}/"
    )
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)
