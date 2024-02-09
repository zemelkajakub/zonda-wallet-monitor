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

    def __init__(self, stats):
        self.stats = stats

    def convertToMailHTML(self):

        data_frame = pd.DataFrame(self.stats)
        data_frame = data_frame.sort_values(by=['pln'], ascending=False)

        table_html = data_frame.to_html(index=False, border=1)

        style_html = open(SOURCE_TABLE_FILE, "r")
        style_html = style_html.read()

        mail_table = str(style_html) + str("\n\n") + str(table_html)
        converted_mail_table = css_inline.inline(mail_table)

        return converted_mail_table

    def sumPLN(self):

        df = pd.DataFrame(self.stats)
        summary = df['pln'].sum()
        summary = round(float(summary), 2)

        return summary


def getCryptoStats(trading_data: ApiConnection, balances_data: ApiConnection) -> List:

    statsArray = []

    owned_currencies = get_owned_currencies(balances_data)
    trading = get_trading(trading_data)
    markets = get_market(owned_currencies)

    for market in markets:

        currency = trading[market]['market']['first']['currency']
        rate = trading[market]['rate']

        funds = owned_currencies[currency]

        plnFloat = float(funds) * float(rate)
        pln = round(plnFloat, 2)

        marketFormatted = re.sub(r'-', ' - ', market)
        currencyStats = {"name": currency, "market": marketFormatted,
                         "funds": funds, "rate": rate, "pln": pln}

        statsArray.append(currencyStats)

    return statsArray


def main():

    url_balances = settings.URL_BALANCES
    url_trading = settings.URL_TRADING
    zonda_api_key = settings.ZONDA_API_KEY
    zonda_api_secret = settings.ZONDA_API_SECRET
    sendgrid_api_key = settings.SENDGRID_API_KEY

    balances_data = ApiConnection(url_balances, zonda_api_key, zonda_api_secret)
    trading_data = ApiConnection(url_trading, zonda_api_key, zonda_api_secret)

    statsData = getCryptoStats(balances_data=balances_data, trading_data=trading_data)
    mail = MailData(statsData)

    table = mail.convertToMailHTML()
    sum_pln = mail.sumPLN()

    message = Mail(
        from_email=settings.SENDER_EMAIL_ADDRESS,
        to_emails=settings.RECEIVER_EMAIL_ADDRESS,
        subject='Daily Crypto Raport',
        html_content="{} <h2> Total amount of PLN: {} </h2>".format(table, sum_pln))

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
