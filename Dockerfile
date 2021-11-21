FROM python:3.10.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /DesafioFIEC

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .