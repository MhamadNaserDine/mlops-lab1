"""
Register the exported champion model (model_export/food11) in the
CONTAINERIZED MLflow server from Docker Compose (Lab 4), then give it
the 'champion' alias so the inference service can load it.
"""
import mlflow
import mlflow.pytorch
from mlflow import MlflowClient

# The mlflow container publishes port 5000 to my PC
mlflow.set_tracking_uri("http://127.0.0.1:5000")
client = MlflowClient()

MODEL_NAME = "food11"
ALIAS = "champion"

# 1. Load the model I exported from my PC's MLflow
model = mlflow.pytorch.load_model("model_export/food11", map_location="cpu")
model.eval()
print("Loaded exported model from model_export/food11")

# 2. Log it into the containerized MLflow and register it as 'food11'
mlflow.set_experiment("food11")
with mlflow.start_run(run_name="import-champion-into-compose"):
    mlflow.set_tag("source", "exported from host MLflow (Lab 3 champion)")
    info = mlflow.pytorch.log_model(
        model,
        name="model",
        serialization_format="pickle",
        registered_model_name=MODEL_NAME,
    )

version = info.registered_model_version
print(f"Registered {MODEL_NAME} version {version}")

# 3. Point the 'champion' alias at it
client.set_registered_model_alias(MODEL_NAME, ALIAS, version)
print(f"Alias '{ALIAS}' -> version {version}")
print("Files stored at:", client.get_logged_model(info.model_id).artifact_location)