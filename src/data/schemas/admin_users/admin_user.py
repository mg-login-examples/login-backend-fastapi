from data.schemas.admin_users.admin_user_base import AdminUserBase
from pydantic import ConfigDict

class AdminUser(AdminUserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
