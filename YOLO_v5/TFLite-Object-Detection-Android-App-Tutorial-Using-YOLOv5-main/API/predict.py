import torch
from PIL import Image

# Load the YOLOv5 model
model_path = 'best.pt'
model = torch.load(model_path, map_location='cpu')['model'].float()  # Load the model and ensure it's in evaluation mode
model.eval()

# Load and preprocess the input image
image_path = '1.jpg'
img = Image.open(image_path)
results = model(img)

# Get prediction information
predictions = results.pred[0]  # Get predictions from the first image in the batch
print(predictions)
