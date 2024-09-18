FROM python:3.12-alpine AS builder  

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app  

COPY requirements.txt .  

RUN apk add --no-cache gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn \
    && apk del gcc musl-dev  

RUN pip install --upgrade pip setuptools


RUN adduser -D appuser  

FROM python:3.12-alpine  

ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

WORKDIR /app  

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages  
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn  

RUN adduser -D appuser  
USER appuser  

COPY --chown=appuser:appuser . .  

ENV FASTAPI_ENV=production  

EXPOSE 8000  

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000"]
