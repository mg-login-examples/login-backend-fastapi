from faker import Faker

from data.schemas.users.user import User
from data.schemas.quotes.quoteCreate import QuoteCreate

fake = Faker(locale='en')

def generate_random_quote_to_create(user: User) -> QuoteCreate:
    quote_text = fake.sentence(nb_words=10, variable_nb_words=True)
    quote = QuoteCreate(text=quote_text, author=user)
    return quote
