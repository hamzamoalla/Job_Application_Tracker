FROM python:3.12-slim

WORKDIR /app

COPY services/classifier-worker/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir \
        torch==2.4.1 \
        --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && pip install --no-cache-dir --force-reinstall \
        torch==2.4.1 \
        --index-url https://download.pytorch.org/whl/cpu \
    && (pip freeze | grep -iE '^nvidia-|^cuda-' | cut -d= -f1 | xargs -r pip uninstall -y) \
    && rm -rf /root/.cache/pip /tmp/*

COPY services/classifier-worker/text_cleaning.py /app/text_cleaning.py
COPY services/classifier-worker/ml_embedding.py /app/ml_embedding.py
COPY services/classifier-worker/ml_ner.py /app/ml_ner.py
COPY services/classifier-worker/worker /app/worker

ENV PYTHONPATH=/app
ENV MODEL_DIR=/app/models
ENV SENTENCE_TRANSFORMERS_HOME=/app/st_cache
ENV HF_HOME=/app/hf_cache

CMD ["python", "-m", "worker.main"]