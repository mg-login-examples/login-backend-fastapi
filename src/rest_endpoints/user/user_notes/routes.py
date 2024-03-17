from pymongo.database import Database
from fastapi import status, Response

from helpers_classes.custom_api_router import APIRouter
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from data.mongo_schemas.user_notes.user_note import UserNote
from data.mongo_schemas.user_notes.user_note_db_table import UserNoteDBTable
from data.mongo_schemas.user_notes.user_note_edit_text_title import UserNote as UserNoteEditTitleText
from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate
from stores.nosql_db_store import crud_base
from .verify_create_user_note_owner_dependency import get_verify_create_user_note_owner_as_fastapi_dependency
from .verify_edit_user_note_owner_dependency import get_verify_edit_user_note_owner_as_fastapi_dependency
from .verify_delete_user_note_owner_dependency import get_verify_delete_user_note_owner_as_fastapi_dependency

def get_router(route_dependencies: CommonRouteDependencies) -> APIRouter:
    router = APIRouter(prefix="/user-notes")

    @router.get('/{user_note_id}', response_model=UserNote, response_model_by_alias=False, dependencies=[route_dependencies.current_user])
    async def get_user_note(user_note_id: str, db: Database = route_dependencies.nosql_database):
        user_notes = crud_base.get_resource_item_by_id(
            db,
            UserNoteDBTable,
            user_note_id,
            ItemSchema=UserNote
        )
        return user_notes

    verify_create_user_note_owner_dependency = get_verify_create_user_note_owner_as_fastapi_dependency(route_dependencies.current_user)
    @router.post('/', response_model=UserNote, response_model_by_alias=False, dependencies=[verify_create_user_note_owner_dependency])
    async def create_user_note(
        user_note_to_create: UserNoteCreate,
        db: Database = route_dependencies.nosql_database
    ):
        user_note = crud_base.create_resource_item(
            db,
            UserNoteDBTable,
            user_note_to_create,
            ItemSchema=UserNote
        )
        return user_note

    verify_edit_user_note_owner_dependency = get_verify_edit_user_note_owner_as_fastapi_dependency(route_dependencies.nosql_database, route_dependencies.current_user)
    @router.put('/{user_note_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[verify_edit_user_note_owner_dependency])
    async def update_user_note(
        user_note_id: str,
        user_note: UserNoteEditTitleText,
        db: Database = route_dependencies.nosql_database
    ):
        crud_base.update_item_by_id(
            db,
            UserNoteDBTable,
            user_note_id,
            user_note,
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    verify_delete_user_note_owner_dependency = get_verify_delete_user_note_owner_as_fastapi_dependency(route_dependencies.nosql_database, route_dependencies.current_user)
    @router.delete('/{user_note_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[verify_delete_user_note_owner_dependency])
    async def delete_user_note(user_note_id: str, db: Database = route_dependencies.nosql_database):
        crud_base.delete_resource_item_by_id(
            db,
            UserNoteDBTable,
            user_note_id
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
