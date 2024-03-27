from random import randint


def get_mock_user_login():
    test_user_email = f"playwright_user{randint(100000, 999999)}@test.com"
    test_password = "12345678"
    return test_user_email, test_password
