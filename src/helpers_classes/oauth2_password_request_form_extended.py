from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm


class OAuth2PasswordRequestFormExtended(OAuth2PasswordRequestForm):

    def __init__(
        self,
        grant_type: str = Form(None, pattern="password"),
        username: str = Form(...),
        password: str = Form(...),
        remember_me: bool = Form(None),
        scope: str = Form(""),
        client_id: str | None = Form(None),
        client_secret: str | None = Form(None),
    ):
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.remember_me = remember_me
