FROM python:3.12-slim

WORKDIR /app

COPY services/classifier-worker/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY text_cleaning.py /app/text_cleaning.py
COPY ml_embedding.py /app/ml_embedding.py
COPY ml_ner.py /app/ml_ner.py
COPY services/classifier-worker/worker.py /app/worker.py

ENV SENTENCE_TRANSFORMERS_HOME=/app/st_cache
ENV HF_HOME=/app/hf_cache

CMD ["python", "worker.py"]