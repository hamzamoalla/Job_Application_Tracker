FROM python:3.12-slim

WORKDIR /app

COPY services/trainer/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ml_embedding.py /app/ml_embedding.py
COPY text_cleaning.py /app/text_cleaning.py
COPY services/trainer/train.py /app/train.py
COPY scripts/seed_training.py /app/seed_training.py

ENV SENTENCE_TRANSFORMERS_HOME=/app/st_cache

CMD ["python", "train.py"]