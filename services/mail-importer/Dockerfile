FROM python:3.12-slim

WORKDIR /app

COPY services/mail-importer/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY services/mail-importer/app /app/app

ENV PYTHONPATH=/app
ENV AUTH_DIR=/app/auth
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
