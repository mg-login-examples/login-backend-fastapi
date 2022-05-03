from data.schemas.admin_users.admin_user_base import AdminUserBase

class AdminUser(AdminUserBase):
    id: int

    class Config:
        orm_mode = True
