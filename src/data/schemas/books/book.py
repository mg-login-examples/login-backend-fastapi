from data.schemas.books.bookBase import BookBase

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
