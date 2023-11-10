from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from PIL import Image
import torch

app = FastAPI()

# Load custom YOLOv5 model
model = torch.load("best.pt", map_location="cpu").autoshape()

# Define endpoint for prediction
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = Path("uploads").joinpath(file.filename)
    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

    # Perform prediction
    img = Image.open(file_path)  # Open the image using PIL
    results = model(img)  # Make predictions on the image

    # Extract class names and confidence scores
    predictions = []
    for det in results.pred[0]:
        class_idx = int(det[-1])
        class_name = model.names[class_idx]  # Get class name from the model's class list
        confidence = float(det[4])  # Confidence score

        # Create a dictionary with class name and confidence score
        prediction_info = {
            "class": class_name,
            "confidence": confidence
        }

        # Append the dictionary to the predictions list
        predictions.append(prediction_info)

    # Return class names and confidence scores
    return predictions
