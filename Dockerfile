FROM python:3.9-slim

WORKDIR /opt/aux_scripts/
COPY aux_scripts/. .

WORKDIR /opt/
COPY divs.py .
COPY requirements.txt .

RUN pip install -r requirements.txt