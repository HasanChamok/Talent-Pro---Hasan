import os
import cv2 as cv
import torch
import numpy as np
import tensorflow as tf
from tkinter import image_names
from unittest import result
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
app = Flask(__name__)

UPLOAD_FOLDER = 'saved'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = torch.hub.load('ultralytics/yolov5','custom', path='best.pt')
classes = []
with open('classes.txt','r') as f:
    for line in f:
        classes.append(line.strip())
        
def detect_image(img_path):
    # label , confidence, Bbox = [] , [] , []
    
    # img = cv.imread(img_path)
    # img = cv.resize(img,(416,416))
    # img_copy = img.copy()  # Create a copy of the original image
    
    
    # results = model(img)
    label, confidence, Bbox = [], [], []
    
    img = cv.imread(img_path)
    img_copy = img.copy()  # Create a copy of the original image
    
    input_size = 416
    img_height, img_width, _ = img.shape
    scale_x, scale_y = img_width / input_size, img_height / input_size
    
    img_resized = cv.resize(img, (input_size, input_size))
    
    results = model(img_resized)
    
    
    for res in results.pandas().xyxy:
        # print(len(res))
        for obj in range(len(res)):
            className = classes[res['class'][obj]]
            label.append(className)
            (x1, y1, x2, y2) = (res['xmin'][obj],res['ymin'][obj],res['xmax'][obj],res['ymax'][obj])
            bbox=(x1,y1,x2,y2)
            # Bbox.append(bbox)
            # confidence.append(res['confidence'][obj])
            # Rescale the coordinates back to the original image size
            x1, y1, x2, y2 = int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y)
            # bbox = (x1, y1, x2, y2)
            Bbox.append(bbox)
            confidence.append(res['confidence'][obj])
            
            # Draw bounding box, confidence score, and label on the copy of the image
            cv.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text = f"{className}: {res['confidence'][obj]:.2f}"
            cv.putText(img_copy, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
    # Save the modified image with bounding boxes, confidence scores, and labels
    img_name = os.path.splitext(os.path.basename(img_path))[0] + "_detections.png"
    img_save_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    cv.imwrite(img_save_path, img_copy)
    
    return label , confidence, Bbox 

def detect_video(vid_path):
    cap = cv.VideoCapture(vid_path)
    
    frames = []
    
    while True:
        ret , frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    
    video_name = os.path.splitext(os.path.basename(vid_path))[0]
    video_folder = os.path.join(app.config['UPLOAD_FOLDER'], video_name)

    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    
    frame_no = 0
    results = []
    saved_frames = []
    
    for frame in frames:
        # results.append(model(frame).pandas().xyxy[0])
        player , football = 0, 0
        detected = model(frame)
        labels, confidences, Bbox, BoundBox = [], [], [], []
        for res in detected.pandas().xyxy:
            for obj in range(len(res)):
                if res['confidence'][obj] > 0.1:  # Confidence threshold
                    label = classes[res['class'][obj]]
                    labels.append(label)
                    if label == 'player':
                        player+=1
                    elif label == 'football':
                        football+=1
                    confidence = res['confidence'][obj]
                    confidences.append(confidence)
                    (x1, y1, x2, y2) = (res['xmin'][obj],res['ymin'][obj],res['xmax'][obj],res['ymax'][obj])
                    bbox=(x1,y1,x2,y2)
                    Bbox.append(bbox)
                    BoundBox.append(bbox)
                    
                    # Save the frame as an image
                    # frame_filename = f"{frame_no}_{label}_{confidence:.2f}.png"
                    # frame_path = os.path.join(app.config['UPLOAD_FOLDER'], frame_filename)
                    # cv.imwrite(frame_path, frame)
                    # saved_frames.append(frame_filename)
                    
                    # Create a dictionary for the current detection result
                    detection_result = {
                        "Frame No" : frame_no,
                        "label": label,
                        "confidence": confidence,
                        "Bounding box": Bbox
                    }
                    results.append(detection_result)
                    Bbox = []
        # Create a copy of the original frame to draw detections on
        frame_with_detections = frame.copy()
        
        for idx, bbox in enumerate(BoundBox):
            # Draw bounding box, confidence score, and label on the frame
            x1, y1, x2, y2 = bbox
            label = labels[idx]
            confidence = confidences[idx]

            # Draw bounding box
            cv.rectangle(frame_with_detections, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # Draw label and confidence score
            text = f"{label}: {confidence:.2f}"
            cv.putText(frame_with_detections, text, (int(x1), int(y1) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2) 
            
            # Save the frame as an image with bounding box, label, and confidence score
            # frame_filename = f"{frame_no}_{labels[idx]}_{confidences[idx]:.2f}.png"
            # frame_path = os.path.join(video_folder, frame_filename)
            # cv.imwrite(frame_path, frame)
        # Save the frame with all detections as an image
        frame_filename = f"{frame_no}_detections.png"
        frame_path = os.path.join(video_folder, frame_filename)
        cv.imwrite(frame_path, frame_with_detections)
        
        print("Frame no : " , frame_no , " Player Detected : " , player , " Football Detected : " , football)          
        frame_no+=1
    # print(results)
    # print(len(results))
    # results = []
    
    return results

@app.route('/upload', methods=['GET','POST'])

def upload_file():
    label , confidence = [] , []
    if request.method == 'POST':
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filePath)
            # return jsonify({'message': 'File uploaded successfully', 'filename': filename})
            if filename.lower().endswith(('png','jpg','jpeg','gif')):
                label, confidence, Bbox = detect_image(filePath)
                return jsonify({"Class": label},{"Bounding Box": Bbox},{"Confidence Score":confidence})
            elif filename.lower().endswith(('.mp4', '.avi', '.mov')):
                results = detect_video(filePath)
                return jsonify({'Results ':  results})
        else:
            return jsonify({'error': 'Invalid file format'})
        
        # label, confidence = detect_image(filePath)
        
    # return jsonify({"Class": label},{"Confidence Score":confidence})
        
        


if __name__ == '__main__':
    app.run(debug=True)
