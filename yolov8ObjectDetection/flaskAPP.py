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


@app.route("/",methods=['GET','POST'])
def predict_img():
    if request.method == 'POST':
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath,'Uploads',f.filename)
            print("Upload Folder is : ", filepath)
            f.save(filepath)
            global imgpath
            predict_img.imgpath = f.filename
            # print( "Printing Predicted Image ::::: ", predict_img)
            
            file_extension = f.filename.rsplit('.',1)[1].lower()
            
            if file_extension == 'jpg':
                img = cv.imread(filepath)
                frame = cv.imencode('.jpg',cv.UMat(img))[1].tobytes()
                
                image = Image.open(io.BytesIO(frame))
                
                #Perfome the detection
                yolo = YOLO('yolov8n.pt')
                # detections = yolo.predict(image,save=True)
                detections = yolo.predict(image)
                print("The detected result is : ", detections)
                return jsonify({"Message" : "Image predicted and saved successfully"})
            elif file_extension == 'mp4':
                video_path = filepath
                cap = cv.VideoCapture(video_path)
                
                #Get Video dimensions
                frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
                
                #Define the codec and create VideoWriter object
                fourcc = cv.VideoWriter_fourcc(*'mp4v')
                out = cv.VideoWriter('outptu.mp4',fourcc, 30.0 , (frame_width,frame_height))
                
                #initialize the yolov8 model here
                model = YOLO('yolov8n.pt')
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    #Do yolo detection on the frame here
                    results = model(frame,save=True)
                    print("The result is : ",results)
                    cv.waitKey(1)
                    
                    res_plotted = results[0].plot()
                    cv.imshow('result',res_plotted)
                    out.write(res_plotted)
                    
                    if cv.waitKey(1) == ord('q'):
                        break
                    
                    for result in results:
                        # class_id, confidence , bbox = result
                        boxes = result.boxes
                        probs = result.probs
                        cls = boxes.cls
                        
                        xyxy = boxes.xyxy
                        xywh = boxes.xywh
                        conf = boxes.conf
                        
                        print(boxes,probs,cls,xyxy,xywh,conf)
                return jsonify({"Message" : "Video detected and saved successfully"})
                    
    # folder_path = 'runs/detect'
    # subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    # latest_subfolders = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    
    # image_path = folder_path + '/' + latest_subfolders + '/' + f.filename                
                    
                    
            
            
if __name__ == '__main__':
    app.run(debug=True)
