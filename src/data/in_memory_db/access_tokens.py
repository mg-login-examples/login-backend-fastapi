from utils.security.access_token_utils import parse_access_token, check_access_tokens_are_equal, check_access_token_is_not_expired

USER_ID_TO_ACCESS_TOKENS = {}

def add_access_token(user_id, access_token):
    if user_id not in USER_ID_TO_ACCESS_TOKENS:
        USER_ID_TO_ACCESS_TOKENS[user_id] = []
    USER_ID_TO_ACCESS_TOKENS[user_id].append(access_token)

def remove_access_token(user_id, access_token):
    if user_id in USER_ID_TO_ACCESS_TOKENS:
        user_tokens = USER_ID_TO_ACCESS_TOKENS[user_id]
        USER_ID_TO_ACCESS_TOKENS[user_id] = [token for token in user_tokens if token != access_token]

def check_if_access_token_is_valid(access_token):
    # TODO Sanitize access_token
    # TODO Check token format is correct
    token_user_id = parse_access_token(access_token, "user_id")
    is_token_valid = False
    if check_access_token_is_not_expired(access_token):
        if token_user_id in USER_ID_TO_ACCESS_TOKENS:
            for user_access_token in USER_ID_TO_ACCESS_TOKENS[token_user_id]:
                if check_access_tokens_are_equal(access_token, user_access_token):
                    is_token_valid = True
    return is_token_valid
