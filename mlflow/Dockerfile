FROM python:3.11-slim

# Same mlflow version as the inference service (avoids client/server mismatch)
RUN pip install --no-cache-dir mlflow==3.16.1

# Folder for the database + artifacts (the named volume is mounted here)
RUN mkdir -p /mlflow-data

EXPOSE 5000

CMD ["mlflow", "server", \
     "--host", "0.0.0.0", "--port", "5000", \
     "--backend-store-uri", "sqlite:////mlflow-data/mlflow.db", \
     "--artifacts-destination", "/mlflow-data/mlruns", \
     "--allowed-hosts", "mlflow,mlflow:5000,localhost,localhost:5000,127.0.0.1,127.0.0.1:5000"]