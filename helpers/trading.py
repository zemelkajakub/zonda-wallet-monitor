from helpers.ApiConnection import ApiConnection


def getTrading(url, apiKey, apiSecret):

    data = ApiConnection(url, apiKey, apiSecret)
    tradingData = data.getData()
    trading = tradingData['items']

    return trading
