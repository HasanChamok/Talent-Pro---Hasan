from flask import send_file
import json
import torch
import cv2 
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
def process_video():
    if request.method == 'POST':
        # Check if the 'file' key is in the request files
        if 'file' in request.files:
            # Get the video file from the request
            video_file = request.files['file']
            
            # Save the video file
            basepath = os.path.dirname(__file__)
            video_path = os.path.join(basepath, 'Uploads', video_file.filename)
            video_file.save(video_path)

            # Open the video file
            cap = cv2.VideoCapture(video_path)

            # Initialize YOLO object detector
            yolo = YOLO('yolov8n.pt')

            # Initialize output data list
            output_data = []
            
            # Get frames per second (fps) of the video
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Define the codec and create a VideoWriter object to save the processed video
            out = cv2.VideoWriter(os.path.join(basepath, 'detected_Videos', 'output.avi'),
                                  cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
                                  (frame_width, frame_height))

            # Loop through the video frames and process them
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                # Convert the frame to PIL Image for YOLO detection
                pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                detections = yolo.predict(pil_frame)[0]  # Access the first element of the returned list

                # Extract bounding boxes, confidence scores, and labels
                boxes = detections.boxes.xyxy.tolist()
                confidences = detections.boxes.conf.tolist()
                class_ids = detections.boxes.cls.tolist()

                # Prepare output data for the frame
                frame_data = []
                # Draw bounding boxes, labels, and confidence scores on the frame
                for i in range(len(boxes)):
                    box = boxes[i]
                    confidence = confidences[i]
                    class_id = int(class_ids[i])
                    label = yolo.names[class_id] if class_id < len(yolo.names) else "Unknown"
                    
                     # Add bounding box, confidence score, and class name to frame data
                    frame_data.append({
                        'box': box,
                        'confidence': confidence,
                        'class_name': label
                    })
                    
                    # Draw bounding box
                    x, y, w, h = map(int, box)
                    color = (0, 255, 0)  # Green color for the bounding box
                    cv2.rectangle(frame, (x, y), (w, h), color, 2)

                    # Add label and confidence score
                    label_text = f"{label}: {confidence:.2f}"
                    cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                # Save annotated frame as an image
                frame_filename = os.path.join(basepath, 'detected_video_frames', f'frame_{int(cap.get(1))}.jpg')
                cv2.imwrite(frame_filename, frame)
                
                #Add frame data to output datalist
                output_data.append(frame_data)

                # Write the frame to the output video
                out.write(frame)

            # Release the video capture and writer objects
            cap.release()
            out.release()

            # Prepare the response JSON
            response_data = {
                'frames': output_data
            }

            return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)