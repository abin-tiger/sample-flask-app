FROM python:3.8

ARG METRICS_FOLDER="metrics_data"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ${METRICS_FOLDER}
ENV METRICS_PORT=9200
ENV PROMETHEUS_MULTIPROC_DIR=./${METRICS_FOLDER}
ENV prometheus_multiproc_dir=./${METRICS_FOLDER}

CMD ["gunicorn", "--config", "config.py", "run:app", "--workers", "2", "--timeout", "10", "--bind", "0.0.0.0:5000"]
