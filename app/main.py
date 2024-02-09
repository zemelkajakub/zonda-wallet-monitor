from helpers.balances import get_owned_currencies, get_market
from helpers.trading import get_trading
from helpers.ApiConnection import ApiConnection
from settings.settings import settings
import pandas as pd
import re
import css_inline
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import List

SOURCE_TABLE_FILE = "html/style.html"


class MailData():

    def __init__(self, stats, market_currency):
        self.stats = stats
        self.market_currency = market_currency.lower()

    def convertToMailHTML(self):

        data_frame = pd.DataFrame(self.stats)
        data_frame = data_frame.sort_values(by=[self.market_currency], ascending=False)

        table_html = data_frame.to_html(index=False, border=1)

        style_html = open(SOURCE_TABLE_FILE, "r")
        style_html = style_html.read()

        mail_table = str(style_html) + str("\n\n") + str(table_html)
        converted_mail_table = css_inline.inline(mail_table)

        return converted_mail_table

    def sumFunds(self):

        df = pd.DataFrame(self.stats)
        summary = df[self.market_currency].sum()
        summary = round(float(summary), 2)

        return summary


def getCryptoStats(trading_data: ApiConnection, balances_data: ApiConnection, market_currency: str) -> List:

    statsArray = []

    owned_currencies = get_owned_currencies(balances_data)
    trading = get_trading(trading_data)
    markets = get_market(owned_currencies)

    market_currency = market_currency.lower()

    for market in markets:

        currency = trading[market]['market']['first']['currency']
        rate = trading[market]['rate']

        funds = owned_currencies[currency]

        market_currency_float = float(funds) * float(rate)
        market_currency_amount = round(market_currency_float, 2)

        marketFormatted = re.sub(r'-', ' - ', market)
        currencyStats = {"name": currency, "market": marketFormatted,
                         "funds": funds, "rate": rate, str(market_currency): market_currency_amount}

        statsArray.append(currencyStats)

    return statsArray


def main():

    url_balances = settings.URL_BALANCES
    url_trading = settings.URL_TRADING
    zonda_api_key = settings.ZONDA_API_KEY
    zonda_api_secret = settings.ZONDA_API_SECRET
    sendgrid_api_key = settings.SENDGRID_API_KEY
    market_currency = settings.MARKET_CURRENCY

    balances_data = ApiConnection(url_balances, zonda_api_key, zonda_api_secret)
    trading_data = ApiConnection(url_trading, zonda_api_key, zonda_api_secret)

    statsData = getCryptoStats(balances_data=balances_data, trading_data=trading_data, market_currency=market_currency)
    mail = MailData(statsData, market_currency=market_currency)

    table = mail.convertToMailHTML()
    sum_funds = mail.sumFunds()

    message = Mail(
        from_email=settings.SENDER_EMAIL_ADDRESS,
        to_emails=settings.RECEIVER_EMAIL_ADDRESS,
        subject='Daily Crypto Raport',
        html_content="{} <h2> Total amount of {}: {} </h2>".format(table, market_currency, sum_funds))

    try:

        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)

    except Exception as e:

        raise e
    
    finally:

        print(response.status_code)
        print(response.body)
        print(response.headers)


if __name__ == "__main__":
    main()
