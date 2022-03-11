from data.schemas.examples.authors.authorBase import AuthorBase

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
