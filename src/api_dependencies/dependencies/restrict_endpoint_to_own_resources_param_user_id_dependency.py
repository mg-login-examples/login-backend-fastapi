import logging

from fastapi import Depends

from data.schemas.users.user import User
from data.schemas.http_error_exceptions.http_403_exceptions import HTTP_403_NOT_AUTHORIZED_EXCEPTION

logger = logging.getLogger(__name__)

def get_restrict_endpoint_to_own_resources_param_user_id_as_fastapi_dependency(
    get_current_user_as_dependency: User
):
    def restrict_endpoint_to_own_resources_param_user_id_dependency(
        user_id: int,
        current_user: User = get_current_user_as_dependency,
    ):
        if user_id != current_user.id:
            raise HTTP_403_NOT_AUTHORIZED_EXCEPTION

    return Depends(restrict_endpoint_to_own_resources_param_user_id_dependency)
