from typing import Any

from fastapi import File, UploadFile, status, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.user import User
from utils.image import image_utils
from data.schemas.http_error_exceptions.http_400_exceptions import HTTP_400_INVALID_IMAGE_TYPE_EXCEPTION


def generate_endpoints(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    current_user_dependency: User,
    restrict_endpoint_to_own_resources_param_user_id: Any
):
    @router.put("/{user_id}/profile-picture",
                dependencies=[restrict_endpoint_to_own_resources_param_user_id])
    async def upload_image(
        sql_db_session: Session = sql_db_session_as_dependency,
        user: User = current_user_dependency,
        image: UploadFile = File(...,
                                 media_type='image/png, image/jpeg, image/jpg'),
    ):
        if not image_utils.check_fastapi_request_uploaded_image_valid(image):
            raise HTTP_400_INVALID_IMAGE_TYPE_EXCEPTION
        image_url = await image_utils.save_image_to_uploads(image)
        user.profile_picture = image_url
        crud_base.update_resource_item_full(sql_db_session, UserModel, user)
        return {"image_url": image_url}

    @router.delete("/{user_id}/profile-picture", dependencies=[
                   restrict_endpoint_to_own_resources_param_user_id], status_code=status.HTTP_204_NO_CONTENT)
    async def delete_image(
        sql_db_session: Session = sql_db_session_as_dependency,
        user: User = current_user_dependency,
    ):
        image_url = user.profile_picture
        if image_url:
            user.profile_picture = None
            crud_base.update_resource_item_full(
                sql_db_session, UserModel, user)
            image_utils.delete_image(image_url)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
