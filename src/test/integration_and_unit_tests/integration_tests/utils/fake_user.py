import random
import string
import logging

from mimesis import Person

from data.schemas.users.userCreate import UserCreate

logger = logging.getLogger(__name__)

person = Person()


def generate_random_user_to_create() -> UserCreate:
    user_email = person.email(domains=["fakegmail.com", "fakeyahoo.com"])
    user_password = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    user = UserCreate(email=user_email, password=user_password)
    return user
