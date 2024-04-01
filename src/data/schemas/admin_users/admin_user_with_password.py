from pydantic import ConfigDict

from data.schemas.admin_users.admin_user_create_as_model import \
    AdminUserCreateAsModel


class AdminUserWithPassword(AdminUserCreateAsModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
