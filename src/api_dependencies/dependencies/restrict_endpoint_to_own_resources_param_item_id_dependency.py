import logging

from fastapi import Depends, HTTPException, status

from data.schemas.users.user import User

logger = logging.getLogger(__name__)

def get_restrict_endpoint_to_own_resources_param_item_id_as_fastapi_dependency(
    get_current_user_as_dependency: User
):
    def restrict_endpoint_to_own_resources_param_item_id_dependency(
        item_id: int,
        current_user: User = get_current_user_as_dependency,
    ):
        if item_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return Depends(restrict_endpoint_to_own_resources_param_item_id_dependency)
