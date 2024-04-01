from fastapi import Response, status
from pymongo.database import Database

from api_dependencies.user_route_dependencies import UserRouteDependencies
from data.mongo_schemas.user_notes.user_note import UserNote
from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate
from data.mongo_schemas.user_notes.user_note_db_table import UserNoteDBTable
from data.mongo_schemas.user_notes.user_note_edit_text_title import \
    UserNote as UserNoteEditTitleText
from helpers_classes.custom_api_router import APIRouter
from stores.nosql_db_store import crud_base

from .verify_create_user_note_owner_dependency import \
    get_verify_create_user_note_owner_as_fastapi_dependency
from .verify_delete_user_note_owner_dependency import \
    get_verify_delete_user_note_owner_as_fastapi_dependency
from .verify_edit_user_note_owner_dependency import \
    get_verify_edit_user_note_owner_as_fastapi_dependency


def get_router(user_route_dependencies: UserRouteDependencies) -> APIRouter:
    router = APIRouter(prefix="/user-notes")

    @router.get(
        "/{user_note_id}",
        response_model=UserNote,
        response_model_by_alias=False,
        dependencies=[user_route_dependencies.current_user],  # type: ignore
    )
    async def get_user_note(
        user_note_id: str, mongo_db: Database = user_route_dependencies.mongo_db
    ):
        user_notes = crud_base.get_resource_item_by_id(
            mongo_db,
            UserNoteDBTable,
            user_note_id,
        )
        return user_notes

    verify_create_user_note_owner_dependency = (
        get_verify_create_user_note_owner_as_fastapi_dependency(
            user_route_dependencies.current_user
        )
    )

    @router.post(
        "/",
        response_model=UserNote,
        response_model_by_alias=False,
        dependencies=[verify_create_user_note_owner_dependency],
    )
    async def create_user_note(
        user_note_to_create: UserNoteCreate,
        mongo_db: Database = user_route_dependencies.mongo_db,
    ):
        user_note = crud_base.create_resource_item(
            mongo_db,
            UserNoteDBTable,
            user_note_to_create,
        )
        return user_note

    verify_edit_user_note_owner_dependency = (
        get_verify_edit_user_note_owner_as_fastapi_dependency(
            user_route_dependencies.mongo_db, user_route_dependencies.current_user
        )
    )

    @router.put(
        "/{user_note_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[verify_edit_user_note_owner_dependency],
    )
    async def update_user_note(
        user_note_id: str,
        user_note: UserNoteEditTitleText,
        mongo_db: Database = user_route_dependencies.mongo_db,
    ):
        crud_base.update_item_by_id(
            mongo_db,
            UserNoteDBTable,
            user_note_id,
            user_note,
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    verify_delete_user_note_owner_dependency = (
        get_verify_delete_user_note_owner_as_fastapi_dependency(
            user_route_dependencies.mongo_db, user_route_dependencies.current_user
        )
    )

    @router.delete(
        "/{user_note_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[verify_delete_user_note_owner_dependency],
    )
    async def delete_user_note(
        user_note_id: str, mongo_db: Database = user_route_dependencies.mongo_db
    ):
        crud_base.delete_resource_item_by_id(mongo_db, UserNoteDBTable, user_note_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
