FROM python:3.10

COPY app /app
COPY .env /app/.env
COPY requirements.txt /app/requirements.txt
COPY entrypoint.sh /entrypoint.sh

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt update && apt upgrade -y

RUN apt install python3-pip -y && \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    chmod +x /entrypoint.sh

ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]
