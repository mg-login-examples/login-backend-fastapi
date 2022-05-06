import os
import logging

from utils.security.access_token_utils import check_access_tokens_are_equal

logger = logging.getLogger(__name__)

class AccessTokenFileStore:
    def __init__(self, file_name: str):
        self.FILE_PATH = os.path.join("data", "access_tokens_store", file_name)
        self.USER_ID_TO_ACCESS_TOKENS = {}
        if os.path.isfile(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as file:
                for line in file:
                    if line.strip("\n"):
                        user_id, access_token = line.strip("\n").split(" ")
                        user_id = int(user_id)
                        if user_id in self.USER_ID_TO_ACCESS_TOKENS:
                            self.USER_ID_TO_ACCESS_TOKENS[user_id].append(access_token)
                        else:
                            self.USER_ID_TO_ACCESS_TOKENS[user_id] = [access_token]
        else:
            with open(self.FILE_PATH, 'a'):
                logger.info(f"Created file: {self.FILE_PATH}")

    def check_access_token_exists(self, token_user_id: int, access_token: str):
        is_token_exists = False
        if token_user_id in self.USER_ID_TO_ACCESS_TOKENS:
            for user_access_token in self.USER_ID_TO_ACCESS_TOKENS[token_user_id]:
                if check_access_tokens_are_equal(access_token, user_access_token):
                    is_token_exists = True
                    break
        return is_token_exists

    def add_access_token_if_not_found(self, user_id: str, access_token: str):
        if not self.check_access_token_exists(user_id, access_token):
            if user_id not in self.USER_ID_TO_ACCESS_TOKENS:
                self.USER_ID_TO_ACCESS_TOKENS[user_id] = []
            self.USER_ID_TO_ACCESS_TOKENS[user_id].append(access_token)
            with open(self.FILE_PATH, 'a') as file:
                file.write(f"{user_id} {access_token}\n")

    def remove_access_token(self, user_id: str, access_token: str):
        if user_id in self.USER_ID_TO_ACCESS_TOKENS:
            user_tokens = self.USER_ID_TO_ACCESS_TOKENS[user_id]
            self.USER_ID_TO_ACCESS_TOKENS[user_id] = [token for token in user_tokens if token != access_token]
            with open(self.FILE_PATH, 'r') as file:
                lines = file.readlines()
            with open(self.FILE_PATH, "w") as file:
                for line in lines:
                    if line.strip("\n") != f"{user_id} {access_token}":
                        file.write(line)
