from data.schemas.users.user import User as UserShallow

class User(UserShallow):
    is_verified: bool
