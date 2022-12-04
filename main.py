from helpers.balances import getOwnedCurrencies, getPlnMarket
from helpers.trading import getTrading
import pandas as pd
import numpy as np
import re
import os
import css_inline
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

URL_TRADING = "https://api.zonda.exchange/rest/trading/ticker"
URL_BALANCES = "https://api.zonda.exchange/rest/balances/BITBAY/balance"
SOURCE_TABLE_FILE = "html/style.html"

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
ZONDA_API_KEY = os.environ.get("ZONDA_API_KEY")
ZONDA_API_SECRET = os.environ.get("ZONDA_API_SECRET")
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")


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


def getCryptoStats():

    statsArray = []

    owned_currencies = getOwnedCurrencies(
        URL_BALANCES, ZONDA_API_KEY, ZONDA_API_SECRET)
    trading = getTrading(URL_TRADING, ZONDA_API_KEY, ZONDA_API_SECRET)
    markets = getPlnMarket(owned_currencies)

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

    statsData = getCryptoStats()
    mail = MailData(statsData)

    table = mail.convertToMailHTML()
    sum_pln = mail.sumPLN()

    message = Mail(
        from_email=EMAIL_ADDRESS,
        to_emails=EMAIL_ADDRESS,
        subject='Daily Crypto Raport',
        html_content="{} <h2> Total amount of PLN funds: {} </h2>".format(table, sum_pln))

    try:

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

    except Exception as e:

        print(e.message)


if __name__ == "__main__":
    main()
