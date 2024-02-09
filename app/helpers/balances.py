from helpers.ApiConnection import ApiConnection
from typing import Dict


def get_owned_currencies(data: ApiConnection) -> Dict[str, float]:

    ownedCrypto = {}

    # data = ApiConnection(url, apiKey, apiSecret)
    currencyList = data.getData()
    currencies = currencyList['balances']

    for i in range(0, len(currencies)):

        if (currencies[i]['totalFunds'] != 0.0) and (currencies[i]['name'] != "PLN"):

            crypto_name = str(currencies[i]['name'])
            crypto_totalfunds = float(currencies[i]['totalFunds'])

            crypto = {crypto_name: crypto_totalfunds}
            ownedCrypto.update(crypto)

    return ownedCrypto


def get_pln_market(owned_currencies):

    markets = []
    owned_currencies = owned_currencies

    for crypto in owned_currencies:
        pln_market = crypto + "-PLN"
        markets.append(pln_market)

    return markets
