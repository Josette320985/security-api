FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY config.py .
COPY crypto_service.py .
COPY rotate_secret.py .

EXPOSE 3000

CMD sh -c "python rotate_secret.py & python app.py"