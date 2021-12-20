FROM python:3.10.1-bullseye
MAINTAINER gmrv

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
