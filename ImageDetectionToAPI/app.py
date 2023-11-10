import os
from tkinter import image_names
from unittest import result
import numpy as np
from flask import Flask, render_template, request
from flask import jsonify
import functions
import random
import torch
import cv2
from werkzeug.utils import secure_filename

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST': 
	# 	#For Videos and image:
	# 	Vid = request.files['image']
	# 	vid_path = "static/" + Vid.filename
	# 	Vid.save(vid_path)

	# 	imges = np.array(functions.yolo(vid_path))
    # 	# imges = functions.yolo(vid_path)
	# 	img = np.asarray(imges)

	# 	ret = functions.check(img)

	# 	val = result[ret]
	# 	print(val)
	# return render_template("index.html", pred = ret, cat = val, vid_name = Vid.filename)
  
		#For images --> 
		img = request.files['image']
		img_path = "static/" + img.filename	
		img.save(img_path)
		img=cv2.imread(img_path)
		img=cv2.resize(img, (416,416))
		label,bbox,confidence,finalResult=functions.yolo(img_path)
		print(finalResult)
		# try:
		# 	os.remove(img_path)
		# except:
		# 	pass
	return jsonify({"label":label},{"bbox":bbox},{"confidence":confidence})
	# return render_template("index.html", prediction = label, img_name = img)
 	
if __name__=='__main__':
	app.run(debug=True)
