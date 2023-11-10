import os
import cv2
import torch
import numpy as np
# import nest_asyncio
# from pyngrok import ngrok
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
classes = []
with open('classes.txt', 'r') as f:
    for line in f:
        classes.append(line.strip())

def detect_objects(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (416, 416))
    results = model(img)
    labels, confidences, Bbox = [], [], []
    for res in results.pandas().xyxy:
        for obj in range(len(res)):
            if res['confidence'][obj] > 0.1:  # Confidence threshold
                labels.append(classes[res['class'][obj]])
                confidences.append(res['confidence'][obj])
                (x1, y1, x2, y2) = (res['xmin'][obj],res['ymin'][obj],res['xmax'][obj],res['ymax'][obj])
                bbox=(x1,y1,x2,y2)
                Bbox.append(bbox)
    return labels, confidences, Bbox, res

@app.route("/detect", methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    img = request.files['image']
    if img.filename == '':
        return jsonify({'error': 'No selected file'})

    img_name = secure_filename(img.filename)
    img_path = 'saved/' + img_name
    img.save(img_path)

    labels, confidences, boundingBox, finalResult = detect_objects(img_path)

    os.remove(img_path)  # Delete the uploaded file after processing

    print(finalResult)
    
    response = {
        'labels': labels,
        'confidences': confidences,
        'Bounding Box' : boundingBox
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)



