import random
import string

from faker import Faker

from admin.data.schemas.users.userCreate import UserCreate

fake = Faker()

def generate_random_user_to_create() -> UserCreate:
    user_email = fake.email()
    user_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    user = UserCreate(email=user_email, password=user_password)
    return user
