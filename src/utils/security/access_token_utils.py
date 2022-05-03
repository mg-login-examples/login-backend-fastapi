import logging
import secrets
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_access_token(user_id: int, expiry_time_seconds: int):
    expiry_datetime_timestamp = int(datetime.now().timestamp()) + expiry_time_seconds
    random_token = ''.join(secrets.token_urlsafe(32).split('-'))[:20]
    return f'{random_token}--{user_id}--{expiry_datetime_timestamp}'

def parse_access_token(access_token: str, value: str = None):
    access_token_random_id = access_token.split('--')[0]
    access_token_user_id = int(access_token.split('--')[1])
    access_token_expiry_timestamp = int(access_token.split('--')[2])
    if not value:
        return access_token_random_id, access_token_user_id, access_token_expiry_timestamp
    if value == "random_id":
        return access_token_random_id
    if value == "user_id":
        return access_token_user_id
    if value == "expiry_timestamp":
        return access_token_expiry_timestamp

def check_access_tokens_are_equal(access_token_1: str, access_token_2: str):
    return secrets.compare_digest(access_token_1, access_token_2)

def check_access_token_is_expired(access_token: str):
    expiry_timestamp = parse_access_token(access_token, "expiry_timestamp")
    if datetime.now().timestamp() < expiry_timestamp:
        return False
    return True
