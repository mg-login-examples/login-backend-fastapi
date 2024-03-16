from data.schemas.examples.authors.authorBase import AuthorBase
from pydantic import ConfigDict

class Author(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
