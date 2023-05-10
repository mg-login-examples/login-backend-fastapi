from typing import List

import requests
from fastapi.encoders import jsonable_encoder

from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate
from data.mongo_schemas.user_notes.user_note import UserNote

def get_user_note(test_client: requests.Session, user_note_id: str) -> UserNote:
    response = test_client.get(f"/api/user-notes/{user_note_id}/")
    assert response.status_code == 200
    return UserNote(**response.json())

def get_user_user_notes(test_client: requests.Session, user_id: int, skip=0, limit=10) -> List[UserNote]:
    response = test_client.get(f"/api/users/{user_id}/user-notes/?skip={skip}&limit={limit}")
    assert response.status_code == 200
    user_notes = [UserNote(**user_note_json) for user_note_json in response.json()]
    return user_notes

def create_user_note(test_client: requests.Session, user_note_to_create: UserNoteCreate) -> UserNote:
    response = test_client.post("/api/user-notes/", json=user_note_to_create.dict())
    assert response.status_code == 200
    return UserNote(**response.json())

def edit_user_note(test_client: requests.Session, user_note_to_edit: UserNote):
    response = test_client.put(f"/api/user-notes/{user_note_to_edit.id}/", json=jsonable_encoder(user_note_to_edit))
    assert response.status_code == 204

def delete_user_note(test_client: requests.Session, user_note_id: str):
    response = test_client.delete(f"/api/user-notes/{user_note_id}/")
    assert response.status_code == 204
