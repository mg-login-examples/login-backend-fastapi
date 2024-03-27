from mimesis import Text

from data.schemas.users.user import User
from data.schemas.quotes.quoteCreate import QuoteCreate

text = Text('en')


def generate_random_quote_to_create(user: User) -> QuoteCreate:
    quote_text = text.quote()
    quote = QuoteCreate(text=quote_text, author=user)
    return quote
