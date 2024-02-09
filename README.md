# Zonda Wallet Monitor - Mailer

by @zemelkajakub

## Usage

### Configuration Variables

The `app/settings/settings.py` file contains the following variables that can delivered from environment variables or `app/.env` file:

- `SENDGRID_API_KEY`: The API key used for authentication to SendGrid - requires an account 
- `ZONDA_API_KEY`: Your personal Zonda API key. It is recomennded to limit permission for that particular key.
- `ZONDA_API_SECRET`: Secret for you personal Zonda API key.
- `SENDER_EMAIL_ADDRESS`: The email address from which email will be sent.
- `RECEIVER_EMAIL_ADDRESS`: The email address to which email will be sent. If not set, then SENDER_EMAIL_ADDRESS will be used.
- `MARKET_CURRENCY`: Currency of the market you want to raport. E.g. PLN

Make sure to set these variables according to your environment before running the application.

### Running with Docker Compose

To run the Wallet Monitor application using Docker Compose, follow these steps:

1. Make sure you have Docker and Docker Compose installed on your machine.
2. Clone the repository: `git clone https://github.com/your-username/wallet-monitor.git`.
3. Navigate to the project directory: `cd wallet-monitor`.
4. Open the `docker-compose.yml` file and update the environment variables with your desired values. Use `.env` file based from `.env.example`
5. Run the application: `docker-compose up --build -d`.

### Running with GitHub Actions

You can also run the Wallet Monitor application using GitHub Actions. However, please note that you need to add the necessary variables and secrets to your repository for it to work correctly.

To run the application using GitHub Actions, follow these steps:

1. Fork the repository to your GitHub account.
2. Navigate to the repository settings and go to the "Secrets" tab.
3. Add the following secrets:

- `SENDGRID_API_KEY`: The API key used for authentication to SendGrid - requires an account 
- `ZONDA_API_KEY`: Your personal Zonda API key. It is recomennded to limit permission for that particular key.
- `ZONDA_API_SECRET`: Secret for you personal Zonda API key.

4. Add the following variables
- `SENDER_EMAIL_ADDRESS`: The email address from which email will be sent.
- `RECEIVER_EMAIL_ADDRESS`: The email address to which email will be sent. If not set, then SENDER_EMAIL_ADDRESS will be used.
- `MARKET_CURRENCY`: Currency of the market you want to raport. E.g. PLN

5. Commit and push any changes to trigger the GitHub Actions workflow. By default pipeline runs on 11:30 AM everyday. 
6. The application will be automatically built and deployed using the provided secrets.

Please ensure that you keep your secrets secure and do not expose them publicly.
