FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install flask psycopg2-binary pandas matplotlib requests python-telegram-bot openpyxl

EXPOSE 5000

CMD ["python3", "main.py"]