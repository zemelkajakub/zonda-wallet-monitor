# Zonda Exchange Wallet Monitor

Small tool for sending formatted table via mail with owned cryptocurrencies and their values in PLN. It additionally sums all PLN funds and display value.  It uses Sendgrid API for sending mails.

Currently it works only for PLN market. (Hope it's going to change soon:)


# Running with docker-compose

## Environment variables

Fill .env file with Zonda API key, API secret, SendGrid API key, sender mail (SendGrid configured sender with API key permissions) and receiver email address.

If RECEIVER_EMAIL_ADDRESS variable will be empty, SENDER_EMAIL_ADDRESS value will be used instead.

## Docker Compose

Run **docker compose up --build -d** and check your address e-mail. :) 
