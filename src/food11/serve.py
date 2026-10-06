import os
from io import BytesIO

import mlflow
import numpy as np
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from torchvision import transforms


app = FastAPI()


MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:5000",
)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

model = mlflow.pyfunc.load_model(
    "models:/food11@champion"
)


CLASS_NAMES = [
    "Bread",
    "Dairy product",
    "Dessert",
    "Egg",
    "Fried food",
    "Meat",
    "Noodles-Pasta",
    "Rice",
    "Seafood",
    "Soup",
    "Vegetable-Fruit",
]


transform = transforms.Compose(
    [
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()

    image = Image.open(
        BytesIO(image_bytes)
    ).convert("RGB")

    tensor = transform(image)

    tensor = tensor.unsqueeze(0)

    input_array = tensor.numpy().astype(
        np.float32
    )

    prediction = model.predict(input_array)

    prediction = np.array(prediction)

    if prediction.ndim == 2:
        logits = prediction[0]

        exp_values = np.exp(
            logits - np.max(logits)
        )

        probabilities = (
            exp_values / exp_values.sum()
        )

        class_index = int(
            np.argmax(probabilities)
        )

        confidence = float(
            probabilities[class_index]
        )

    else:
        class_index = int(prediction[0])
        confidence = 1.0

    return {
        "category": CLASS_NAMES[class_index],
        "confidence": confidence,
    }
# Q4 cache test: small change to serve.py
