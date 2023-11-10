from flask import send_file
import json
import torch
import cv2 as cv
import numpy
import tensorflow as tf
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, Response, jsonify
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from subprocess import Popen
import re
import requests
import shutil
import time
import glob
import io
from PIL import Image
import datetime
import argparse

from ultralytics import YOLO

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def predict_img():
    if request.method == 'POST':
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath, 'Uploads', f.filename)
            f.save(filepath)

            # Perform the detection
            yolo = YOLO('yolov8n.pt')
            image = Image.open(filepath)
            detections = yolo.predict(image)[0]  # Access the first element of the returned list

            # Extract bounding boxes, confidence scores, and labels
            boxes = detections.boxes.xyxy.tolist()  # Convert to a list for JSON serialization
            confidences = detections.boxes.conf.tolist()  # Extract confidence values
            class_ids = detections.boxes.cls.tolist()  # Extract class values
            
            # Get class names corresponding to class IDs
            class_names = [yolo.names[class_id] if class_id < len(yolo.names) else "Unknown" for class_id in class_ids]

            # Draw bounding boxes, labels, and confidence scores on the detected image
            detected_image = cv.cvtColor(detections.orig_img, cv.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
            
            # Prepare the response data
            detected_objects = []
            for i in range(len(boxes)):
                box = boxes[i]
                confidence = confidences[i]
                class_id = int(class_ids[i])   # Get the index of the class with the highest confidence
                label = class_names[i]  # Use class names instead of class IDs  # Check if class_id is within the range of class names
                
                # Draw bounding box
                x, y, w, h = map(int, box)
                color = (0, 255, 0)  # Green color for the bounding box
                cv.rectangle(detected_image, (x, y), (w, h), color, 2)
                
                # Add label and confidence score
                label_text = f"{label}: {confidence:.2f}"
                cv.putText(detected_image, label_text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            # Save the detected image
            detected_image_path = os.path.join(basepath, 'Detected_Images', f.filename)
            cv.imwrite(detected_image_path, detected_image)

            # Prepare the response JSON
            response_data = {
                'detected_objects': {
                    'labels': class_names,
                    'confidences': confidences,
                    'boxes': boxes
                },
                'detected_image_path': detected_image_path
            }
            
            return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)