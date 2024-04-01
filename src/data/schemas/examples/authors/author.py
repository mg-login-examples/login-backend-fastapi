from pydantic import ConfigDict

from data.schemas.examples.authors.authorBase import AuthorBase


class Author(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
