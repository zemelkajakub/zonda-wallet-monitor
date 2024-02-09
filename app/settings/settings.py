from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    URL_TRADING: str = "https://api.zonda.exchange/rest/trading/ticker"
    URL_BALANCES: str = "https://api.zonda.exchange/rest/balances/BITBAY/balance"
    SENDER_EMAIL_ADDRESS: str = os.environ.get("SENDER_EMAIL_ADDRESS")
    RECEIVER_EMAIL_ADDRESS: str = os.environ.get(
        "RECEIVER_EMAIL_ADDRESS") or SENDER_EMAIL_ADDRESS
    SENDGRID_API_KEY: str = os.environ.get("SENDGRID_API_KEY")
    ZONDA_API_KEY: str = os.environ.get("ZONDA_API_KEY")
    ZONDA_API_SECRET: str = os.environ.get("ZONDA_API_SECRET")
    MARKET_CURRENCY: str = os.environ.get("MARKET_CURRENCY", "PLN")

    class Config:
        env_file = ".env"


settings = Settings()
