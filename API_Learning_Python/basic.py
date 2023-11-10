import os
from flask import Flask,jsonify,request


app = Flask(__name__)

@app.route("/")

def Home():
    return "Home"

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
# GET ---> Request data from a specified resource
# POST ---> Create a resource
# PUT ---> Update a resource
# DELETE ---> Delete a resource