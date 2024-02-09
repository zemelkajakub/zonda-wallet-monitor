from helpers.ApiConnection import ApiConnection
from typing import Dict
from settings.settings import settings


def get_owned_currencies(data: ApiConnection) -> Dict[str, float]:

    ownedCrypto = {}
    currencyList = data.getData()
    currencies = currencyList['balances']

    for i in range(0, len(currencies)):

        if (currencies[i]['totalFunds'] != 0.0) and (currencies[i]['name'] != "PLN"):

            crypto_name = str(currencies[i]['name'])
            crypto_totalfunds = float(currencies[i]['totalFunds'])

            crypto = {crypto_name: crypto_totalfunds}
            ownedCrypto.update(crypto)

    return ownedCrypto


def get_market(owned_currencies):

    markets = []
    owned_currencies = owned_currencies
    market_currency = settings.MARKET_CURRENCY 

    for crypto in owned_currencies:
        market = crypto + f"-{market_currency}"
        markets.append(market)

    return markets
