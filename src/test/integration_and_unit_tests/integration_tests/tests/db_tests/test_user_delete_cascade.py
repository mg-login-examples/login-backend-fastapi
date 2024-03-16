import logging
from datetime import datetime

from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from data.database.models.user import User as UserModel
from data.database.models.quote import Quote as QuoteModel
from data.database.models.user_email_verification import UserEmailVerification as UserEmailVerificationModel
from data.database.models.user_session import UserSession as UserSessionModel
from data.database.models.user_password_reset_token import UserPasswordResetToken as UserPasswordResetTokenModel
from data.database.models.user_quote_like import UserQuoteLike as UserQuoteLikeModel
from data.endUserSchemasToDbSchemas.user import createSchemaToDbSchema as userCreateSchemaToDbSchema
from data.endUserSchemasToDbSchemas.quote import createSchemaToDbSchema as quoteCreateSchemaToDbSchema

from data.schemas.users.userDeep import User as UserDeep
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.user_email_verifications.userEmailVerificationBase import UserEmailVerificationBase
from data.schemas.user_sessions.userSessionCreate import UserSessionCreate
from data.schemas.user_password_reset_tokens.userPasswordResetTokenBase import UserPasswordResetTokenBase
from data.schemas.user_quote_like.user_quote_like import UserQuoteLike
from stores.sql_db_store import crud_base
from test.integration_and_unit_tests.integration_tests.utils.fake_user import generate_random_user_to_create
from test.integration_and_unit_tests.integration_tests.utils.fake_quote import generate_random_quote_to_create

logger = logging.getLogger(__name__)

def test_user_delete_cascade_quotes(app_db_manager: SQLAlchemyDBManager):
    db_session = next(app_db_manager.db_session())
    # create user
    user_login = generate_random_user_to_create()
    user_password_hashed = userCreateSchemaToDbSchema(user_login)
    user_db = crud_base.create_resource_item(db_session, UserModel, user_password_hashed)
    user = UserDeep.model_validate(user_db)
    # create user quote
    quote_to_create = generate_random_quote_to_create(user)
    quote_to_create = quoteCreateSchemaToDbSchema(quote_to_create)
    quote_db = crud_base.create_resource_item(db_session, QuoteModel, quote_to_create)
    quote = QuoteDeep.model_validate(quote_db)
    # given a user with quotes
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    user = UserDeep.model_validate(user_db)
    assert len(user.quotes) == 1
    assert user.quotes[0].id == quote.id
    # if the user is deleted
    crud_base.delete_resource_item(db_session, UserModel, user.id)
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    assert user_db is None
    # the user quotes are also deleted
    quote_db = crud_base.get_resource_item(db_session, QuoteModel, quote.id)
    assert quote_db is None

def test_user_delete_cascade_email_verifications(app_db_manager: SQLAlchemyDBManager):
    db_session = next(app_db_manager.db_session())
    # create user
    user_login = generate_random_user_to_create()
    user_password_hashed = userCreateSchemaToDbSchema(user_login)
    user_db = crud_base.create_resource_item(db_session, UserModel, user_password_hashed)
    user = UserDeep.model_validate(user_db)
    # create user email verification
    email_verification = UserEmailVerificationBase(user_id=user.id, verification_code='132213', expires_at=datetime.now())
    email_verification_db = crud_base.create_resource_item(db_session, UserEmailVerificationModel, email_verification)
    email_verification_id = email_verification_db.id
    # given a user with email verifications
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    user = UserDeep.model_validate(user_db)
    email_verification_db = crud_base.get_resource_item(db_session, UserEmailVerificationModel, email_verification_id)
    assert email_verification_db.user_id == user.id
    # if the user is deleted
    crud_base.delete_resource_item(db_session, UserModel, user.id)
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    assert user_db is None
    # the user's email verifications are also deleted
    email_verification_db = crud_base.get_resource_item(db_session, UserEmailVerificationModel, email_verification_id)
    assert email_verification_db is None

def test_user_delete_cascade_user_sessions(app_db_manager: SQLAlchemyDBManager):
    db_session = next(app_db_manager.db_session())
    # create user
    user_login = generate_random_user_to_create()
    user_password_hashed = userCreateSchemaToDbSchema(user_login)
    user_db = crud_base.create_resource_item(db_session, UserModel, user_password_hashed)
    user = UserDeep.model_validate(user_db)
    # create user session
    user_session_create = UserSessionCreate(user_id=user.id, token='132213', expires_at=datetime.now())
    user_session_db = crud_base.create_resource_item(db_session, UserSessionModel, user_session_create)
    user_session_id = user_session_db.id
    # given a user with user sessions
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    user = UserDeep.model_validate(user_db)
    user_session_db = crud_base.get_resource_item(db_session, UserSessionModel, user_session_id)
    assert user_session_db.user_id == user.id
    # if the user is deleted
    crud_base.delete_resource_item(db_session, UserModel, user.id)
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    assert user_db is None
    # the user's user sessions are also deleted
    user_session_db = crud_base.get_resource_item(db_session, UserSessionModel, user_session_id)
    assert user_session_db is None

def test_user_delete_cascade_password_tokens(app_db_manager: SQLAlchemyDBManager):
    db_session = next(app_db_manager.db_session())
    # create user
    user_login = generate_random_user_to_create()
    user_password_hashed = userCreateSchemaToDbSchema(user_login)
    user_db = crud_base.create_resource_item(db_session, UserModel, user_password_hashed)
    user = UserDeep.model_validate(user_db)
    # create user password token
    password_token = UserPasswordResetTokenBase(user_id=user.id, token=132213, expires_at=datetime.now(), is_active=False)
    password_token_db = crud_base.create_resource_item(db_session, UserPasswordResetTokenModel, password_token)
    password_token_id = password_token_db.id
    # given a user with password tokens
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    user = UserDeep.model_validate(user_db)
    password_token_db = crud_base.get_resource_item(db_session, UserPasswordResetTokenModel, password_token_id)
    assert password_token_db.user_id == user.id
    # if the user is deleted
    crud_base.delete_resource_item(db_session, UserModel, user.id)
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    assert user_db is None
    # the user's password tokens are also deleted
    password_token_db = crud_base.get_resource_item(db_session, UserPasswordResetTokenModel, password_token_id)
    assert password_token_db is None

def test_user_delete_cascade_quote_likes(app_db_manager: SQLAlchemyDBManager):
    db_session = next(app_db_manager.db_session())
    # create main user
    user_login = generate_random_user_to_create()
    user_password_hashed = userCreateSchemaToDbSchema(user_login)
    user_db = crud_base.create_resource_item(db_session, UserModel, user_password_hashed)
    user = UserDeep.model_validate(user_db)
    # create user 2 (quote author) and quote
    user_2_login = generate_random_user_to_create()
    user_2_password_hashed = userCreateSchemaToDbSchema(user_2_login)
    user_2_db = crud_base.create_resource_item(db_session, UserModel, user_2_password_hashed)
    user_2 = UserDeep.model_validate(user_2_db)
    quote_to_create = generate_random_quote_to_create(user_2)
    quote_to_create = quoteCreateSchemaToDbSchema(quote_to_create)
    quote_db = crud_base.create_resource_item(db_session, QuoteModel, quote_to_create)
    quote = QuoteDeep.model_validate(quote_db)
    # create user quote like
    user_quote_like = UserQuoteLike(user_id=user.id, quote_id=quote.id)
    crud_base.create_resource_item(db_session, UserQuoteLikeModel, user_quote_like)
    # given a user with quote likes
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    user = UserDeep.model_validate(user_db)
    assert len(user.liked_quotes) == 1
    assert user.liked_quotes[0].id == quote.id
    # if the user is deleted
    crud_base.delete_resource_item(db_session, UserModel, user.id)
    user_db = crud_base.get_resource_item(db_session, UserModel, user.id)
    assert user_db is None
    # the user's quote likes are also deleted
    quote_db = crud_base.get_resource_item(db_session, QuoteModel, quote.id)
    quote = QuoteDeep.model_validate(quote_db)
    assert len(quote.liked_by_users) == 0
    user_quote_like = crud_base.get_resource_item_by_attribute(db_session, UserQuoteLikeModel, UserQuoteLikeModel.user_id, user.id)
    assert user_quote_like is None
    user_quote_like = crud_base.get_resource_item_by_attribute(db_session, UserQuoteLikeModel, UserQuoteLikeModel.quote_id, quote.id)
    assert user_quote_like is None
