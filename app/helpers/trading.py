from helpers.ApiConnection import ApiConnection
from typing import Dict

def get_trading(data: ApiConnection) -> Dict:

    tradingData = data.getData()
    trading = tradingData['items']

    return trading
