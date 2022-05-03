from data.schemas.admin_users.admin_user_base import AdminUserBase

class AdminUserCreateAsModel(AdminUserBase):
    hashed_password: str
