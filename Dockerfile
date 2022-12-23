# syntax=docker/dockerfile:1.3
FROM python:3.10-alpine

WORKDIR /shop-api

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY . .

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade -r requirements.txt