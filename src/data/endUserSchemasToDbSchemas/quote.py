from data.schemas.quotes.quoteCreate import QuoteCreate as QuoteCreateSchema
from data.schemas.quotes.quoteCreateAsModel import QuoteCreateAsModel as QuoteCreateAsModelSchema
from data.schemas.quotes.quoteDeep import Quote as QuoteDeepSchema
from data.schemas.quotes.quoteUpdateAsModel import QuoteUpdateAsModel as QuoteUpdateAsModelSchema

def createSchemaToDbSchema(quote: QuoteCreateSchema) -> QuoteCreateAsModelSchema:
    quote_as_model = QuoteCreateAsModelSchema(**quote.dict(exclude={'author'}), author_id=quote.author.id)
    return quote_as_model

def updateSchemaToDbSchema(quote: QuoteDeepSchema) -> QuoteUpdateAsModelSchema:
    quote_as_model = QuoteUpdateAsModelSchema(**quote.dict(exclude={'author'}), author_id=quote.author.id)
    quote_as_model.author_id = quote.author.id
    return quote_as_model
