"""
Export the current champion model (food11@champion) from the MLflow
server running on my PC to a local folder, so it can be registered
later in the new containerized MLflow server (Lab 4).
"""
import shutil
from pathlib import Path

import mlflow
import mlflow.pytorch

mlflow.set_tracking_uri("http://127.0.0.1:5000")

EXPORT_DIR = Path("model_export/food11")

# Start from a clean folder
if EXPORT_DIR.exists():
    shutil.rmtree(EXPORT_DIR)
EXPORT_DIR.parent.mkdir(exist_ok=True)

# Load the current champion and save it as a local MLflow model folder
model = mlflow.pytorch.load_model("models:/food11@champion", map_location="cpu")
model.eval()
mlflow.pytorch.save_model(model, str(EXPORT_DIR), serialization_format="pickle")

print("Exported champion model to:", EXPORT_DIR.resolve())
for f in sorted(EXPORT_DIR.rglob("*")):
    if f.is_file():
        print(f"  {f.relative_to(EXPORT_DIR)}  ({f.stat().st_size / 1e6:.1f} MB)")