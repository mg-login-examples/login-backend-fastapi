import requests

from data.schemas.users.user import User
from data.schemas.login.login_response import LoginResponse
from data.schemas.users.userCreate import UserCreate


def verify_email(test_client: requests.Session, verification_code: int) -> User:
    response = test_client.post(f"/api/email-verifications/verify-email/{verification_code}")
    assert response.status_code == 204

def resend_verification_email(test_client: requests.Session):
    response = test_client.post("/api/email-verifications/resend-email/")
    assert response.status_code == 204
