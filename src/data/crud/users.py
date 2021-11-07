# from sqlalchemy.orm import Session

# from data.schemas import users as userSchemas
# from data.database.models.user import User as UserModel

# def get_user(db: Session, user_id: int) -> UserModel:
#     return db.query(UserModel).filter(UserModel.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(UserModel).filter(UserModel.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(UserModel).offset(skip).limit(limit).all()


# def create_user(db: Session, user: userSchemas.UserCreate) -> UserModel:
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = UserModel(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
