from admin.data.schemas.examples.books.bookBase import BookBase

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
