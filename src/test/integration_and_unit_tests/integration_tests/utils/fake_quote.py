from mimesis import Text

from data.schemas.quotes.quoteCreate import QuoteCreate
from data.schemas.users.user import User

text = Text("en")


def generate_random_quote_to_create(user: User) -> QuoteCreate:
    quote_text = text.quote()
    quote = QuoteCreate(text=quote_text, author=user)
    return quote
