from data.schemas.admin_users.admin_user_create_as_model import AdminUserCreateAsModel

class AdminUserWithPassword(AdminUserCreateAsModel):
    id: int

    class Config:
        orm_mode = True