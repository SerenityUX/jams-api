FROM python:3.9-slim

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install slack-bolt pyairtable 