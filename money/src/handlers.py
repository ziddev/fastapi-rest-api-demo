from fastapi import APIRouter, HTTPException

from http_tool import fetch_data
from models import CurrencyConversionRequest


EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
CRYPTO_LIST_URL = "https://api.coingecko.com/api/v3/coins/list"
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"


router = APIRouter(prefix="/api/v1")


@router.get("/currencies", tags=["currency"])
def list_currencies():
    return {"available_currencies": list(fetch_data(EXCHANGE_API_URL).get("rates", {}).keys())}


@router.get("/currencies/exchange-rate/{currency}", tags=["currency"])
def get_exchange_rate(currency: str):
    rates = fetch_data(EXCHANGE_API_URL).get("rates", {})
    if currency.upper() not in rates:
        raise HTTPException(status_code=404, detail="Devise non trouvée")
    return {"currency": currency.upper(), "exchange_rate": rates[currency.upper()]}


@router.post("/currencies/convert", tags=["currency"])
def convert_currency(req: CurrencyConversionRequest):
    rates = fetch_data(EXCHANGE_API_URL).get("rates", {})
    if req.from_currency.upper() not in rates or req.to_currency.upper() not in rates:
        raise HTTPException(status_code=404, detail="Devise non trouvée")
    return {
        "from_currency": req.from_currency.upper(),
        "to_currency": req.to_currency.upper(),
        "amount": req.amount,
        "converted_amount": round((req.amount / rates[req.from_currency.upper()]) * rates[req.to_currency.upper()], 2)
    }


@router.get("/cryptos", tags=["crypto"])
def list_cryptos():
    """ Liste toutes les cryptos disponibles """
    return {"available_cryptos": [crypto["id"] for crypto in fetch_data(CRYPTO_LIST_URL)]}


@router.get("/cryptos/{crypto}", tags=["crypto"])
def get_crypto_price(crypto: str):
    data = fetch_data(CRYPTO_API_URL, {"ids": crypto.lower(), "vs_currencies": "usd"})
    if crypto.lower() not in data:
        raise HTTPException(status_code=404, detail="Cryptomonnaie non trouvée")
    return {"crypto": crypto.upper(), "price_usd": data[crypto.lower()]["usd"]}
