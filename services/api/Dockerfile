FROM python:3.12-slim

WORKDIR /app

COPY services/api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY services/api/app.py /app/app.py
COPY text_cleaning.py /app/text_cleaning.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]