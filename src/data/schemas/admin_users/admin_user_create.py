from data.schemas.admin_users.admin_user_base import AdminUserBase

class AdminUserCreate(AdminUserBase):
    password: str
