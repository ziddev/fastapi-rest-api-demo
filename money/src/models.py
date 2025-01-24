from pydantic import BaseModel


class CurrencyConversionRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
