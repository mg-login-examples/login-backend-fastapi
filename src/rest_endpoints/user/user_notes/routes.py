from typing import List

from pymongo.database import Database
from fastapi import status, Response

from helpers_classes.custom_api_router import APIRouter
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from data.mongo_schemas.user_notes.user_note import UserNote
from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate
from stores.nosql_db_store import crud_base

def get_router(route_dependencies: CommonRouteDependencies) -> APIRouter:
    router = APIRouter(prefix="/user-notes")

    @router.get('/count', response_model=int)
    async def get_user_notes_count(db: Database = route_dependencies.nosql_database):
        user_notes_count = crud_base.get_resource_items_count(db, "user_notes")
        return user_notes_count

    @router.get('/', response_model=List[UserNote], response_model_by_alias=False)
    async def get_user_notes(
        skip: int = 0,
        limit: int = 100,
        db: Database = route_dependencies.nosql_database
    ):
        user_notes = crud_base.get_resource_items(
            db,
            "user_notes",
            ItemSchema=UserNote,
            limit=limit,
            skip=skip
        )
        return user_notes

    @router.get('/{user_note_id}', response_model=UserNote, response_model_by_alias=False)
    async def get_user_note(user_note_id: str, db: Database = route_dependencies.nosql_database):
        user_notes = crud_base.get_resource_item_by_id(
            db,
            "user_notes",
            user_note_id,
            ItemSchema=UserNote
        )
        return user_notes

    @router.post('/', response_model=UserNote, response_model_by_alias=False)
    async def create_user_note(
        user_note_to_create: UserNoteCreate,
        db: Database = route_dependencies.nosql_database
    ):
        user_note = crud_base.create_resource_item(
            db,
            "user_notes",
            user_note_to_create,
            ItemSchema=UserNote
        )
        return user_note

    @router.put('/{user_note_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def update_user_note(
        user_note_id: str,
        user_note_to_update: UserNote,
        db: Database = route_dependencies.nosql_database
    ):
        crud_base.update_item_by_id(
            db,
            "user_notes",
            user_note_id,
            user_note_to_update,
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.delete('/{user_note_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user_note(user_note_id: str, db: Database = route_dependencies.nosql_database):
        crud_base.delete_resource_item_by_id(
            db,
            "user_notes",
            user_note_id
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
