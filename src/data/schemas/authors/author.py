from data.schemas.authors.authorBase import AuthorBase

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
