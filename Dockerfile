FROM ubuntu:20.04

WORKDIR /app

COPY . .

RUN apt update 

RUN apt install python3-pip -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["/usr/bin/python3", "main.py"]
