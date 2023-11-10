import os
from flask import Flask, jsonify, request
from roboflow import Roboflow
from subprocess import run, PIPE, Popen

app = Flask(__name__)

# Set up Roboflow API key and project details
roboflow_api_key = "YOUR_ROBOFLOW_API_KEY"
project_name = "cats-and-dogs-fetbf"
version_number = 1

@app.route('/detect_nudity', methods=['POST'])
def detect_nudity():
    # Get the uploaded image file
    image_file = request.files['image']

    # Save the image temporarily
    image_path = "temp_image.jpg"
    image_file.save(image_path)

    # Run YOLO detection using the specified model
    process = Popen(
        f"yolo task=detect mode=predict model=/content/runs/detect/train4/weights/best.pt conf=0.5 source={image_path}",
        stdout=PIPE, stderr=PIPE, shell=True
    )
    output, error = process.communicate()

    # Process the output or error as needed

    # Clean up the temporary image file
    os.remove(image_path)

    return jsonify({'result': output.decode('utf-8')})


if __name__ == '__main__':
    app.run(debug=True)
