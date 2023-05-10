from typing import List
import logging

import requests
from fastapi.encoders import jsonable_encoder

from data.mongo_schemas.user_notes.user_note import UserNote
from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate
from test.integration_and_unit_tests.integration_tests.utils import asserts

logger = logging.getLogger(__name__)

def get_user_note(test_client: requests.Session, user_note_id: int) -> UserNote:
    response = test_client.get(f"/api/admin/resource/user-notes/{user_note_id}/")
    assert response.status_code == 200
    return UserNote(**response.json())

def create_user_note(test_client: requests.Session, user_note_to_create: UserNoteCreate) -> UserNote:
    response = test_client.post("/api/admin/resource/user-notes/", json=user_note_to_create.dict())
    assert response.status_code == 200
    return UserNote(**response.json())

def put_user_note(test_client: requests.Session, user_note_to_edit: UserNote):
    response = test_client.put(f"/api/admin/resource/user-notes/{user_note_to_edit.id}/", json=jsonable_encoder(user_note_to_edit))
    assert response.status_code == 204

def delete_user_note(test_client: requests.Session, user_note_id: int):
    response = test_client.delete(f"/api/admin/resource/user-notes/{user_note_id}/")
    assert response.status_code == 204

def get_user_notes(test_client: requests.Session, skip=0, limit=10) -> List[UserNote]:
    response = test_client.get(f"/api/admin/resource/user-notes/?skip={skip}&limit={limit}")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    user_notes = [UserNote(**user_note_json) for user_note_json in response.json()]
    return user_notes

def get_user_note_expect_not_found(test_client: requests.Session, user_note_id: int):
    response = test_client.get(f"/api/admin/resource/user-notes/{user_note_id}/")
    assert response.status_code == 404
    asserts.assert_response_error_item_not_found(response)
