# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libev-dev \
    python3-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY download.py download.py
RUN python3 download.py

COPY . .

# Limit upload size to 16 Mb
ENV MAX_CONTENT_LENGTH=16777216

CMD python3 app.py

