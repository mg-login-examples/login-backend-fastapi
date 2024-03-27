from pydantic import BaseModel


class GoogleSignInPayload(BaseModel):
    clientId: str
    client_id: str
    credential: str
    select_by: str
