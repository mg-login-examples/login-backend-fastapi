from typing import Any

from fastapi import File, UploadFile, HTTPException, status, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.user import User
from utils.image import image_utils


def generate_endpoints(
    router: APIRouter,
    db_as_dependency: Session,
    current_user_dependency: User,
    restrict_endpoint_to_own_resources_param_user_id: Any
):
    @router.put("/{user_id}/profile-picture", dependencies=[restrict_endpoint_to_own_resources_param_user_id])
    async def upload_image_response(
        db: Session = db_as_dependency,
        user: User = current_user_dependency,
        image: UploadFile = File(..., media_type='image/png, image/jpeg, image/jpg'),
    ):
        if not image_utils.check_fastapi_request_uploaded_image_valid(image):
            raise HTTPException(status_code=400, detail="Invalid file type. Only PNG and JPEG/JPG files are allowed.")
        image_url = await image_utils.save_image_to_uploads(image)
        user.profile_picture = image_url
        crud_base.update_resource_item_full(db, UserModel, user)
        return { "image_url": image_url }

    @router.delete("/{user_id}/profile-picture", dependencies=[restrict_endpoint_to_own_resources_param_user_id], status_code=status.HTTP_204_NO_CONTENT)
    async def upload_image_response(
        db: Session = db_as_dependency,
        user: User = current_user_dependency,
    ):
        image_url = user.profile_picture
        if image_url:
            user.profile_picture = None
            crud_base.update_resource_item_full(db, UserModel, user)
            image_utils.delete_image(image_url)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
