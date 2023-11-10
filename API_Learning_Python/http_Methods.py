#GET REQUEST
from flask import Flask,jsonify,request


app = Flask(__name__)

@app.route("/get-user/<user_id>")

def get_user(user_id):
    user_data = {
        "user_id" : user_id,
        "name" : "Hasan",
        "email" : "hasan.chamok16@gmail.com"
    }
    
    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
# GET ---> Request data from a specified resource
# POST ---> Create a resource
# PUT ---> Update a resource
# DELETE ---> Delete a resource