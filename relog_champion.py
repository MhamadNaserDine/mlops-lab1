"""
Re-log the current champion model so its files are stored THROUGH
the MLflow server (mlflow-artifacts:/) instead of a local Windows path.
Then register it as a new version of 'food11' and move the 'champion'
alias to that new version.
"""
import mlflow
import mlflow.pytorch
from mlflow import MlflowClient

mlflow.set_tracking_uri("http://127.0.0.1:5000")
client = MlflowClient()

MODEL_NAME = "food11"
ALIAS = "champion"
EXP_NAME = "food11-serving"

# 1. Find the current champion version and the run it came from
old = client.get_model_version_by_alias(MODEL_NAME, ALIAS)
print(f"Current champion: version {old.version} (run {old.run_id})")

# 2. Load that model on Windows (where its files exist)
model = mlflow.pytorch.load_model(f"models:/{MODEL_NAME}@{ALIAS}", map_location="cpu")
model.eval()
print("Loaded current champion model.")

# 3. Create (or reuse) an experiment whose artifacts go through the server
exp = client.get_experiment_by_name(EXP_NAME)
if exp is None:
    exp_id = client.create_experiment(
        EXP_NAME,
        artifact_location="mlflow-artifacts:/food11-serving",
    )
else:
    exp_id = exp.experiment_id
mlflow.set_experiment(experiment_id=exp_id)

# 4. Re-log the same model + copy the original metrics, and register it
old_run = client.get_run(old.run_id)
with mlflow.start_run(run_name="champion-relogged-for-docker"):
    mlflow.set_tag("copied_from_run", old.run_id)
    mlflow.set_tag("copied_from_version", old.version)
    mlflow.log_metrics(old_run.data.metrics)
    info = mlflow.pytorch.log_model(
        model,
        name="model",
        serialization_format="pickle",
        registered_model_name=MODEL_NAME,
    )

new_version = info.registered_model_version
print(f"Registered new version: {new_version}")

# 5. Move the champion alias to the new version
client.set_registered_model_alias(MODEL_NAME, ALIAS, new_version)
print(f"Alias '{ALIAS}' now points to version {new_version}")

# 6. Show where the new model files are stored
print("New files stored at:", client.get_logged_model(info.model_id).artifact_location)