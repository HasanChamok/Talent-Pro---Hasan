# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 18:50:57 2022

@author: siddhardhan
"""

from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json


app = FastAPI()

class model_input(BaseModel):
    
    pregnancies : int
    Glucose : int
    BloodPressure : int
    SkinThickness : int
    Insulin : int
    BMI : float
    DiabetesPedigreeFunction : float
    Age : int       
        
# loading the saved model
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

@app.post('/diabetes_prediction')
def diabetes_predd(input_parameters : model_input):
    
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    
    preg = input_dictionary['Pregnancies']
    glu = input_dictionary['Glucose']
    bp = input_dictionary['BloodPressure']
    skin = input_dictionary['SkinThickness']
    insulin = input_dictionary['Insulin']
    bmi = input_dictionary['BMI']
    dpf = input_dictionary['DiabetesPedigreeFunction']
    age = input_dictionary['Age']
    
    
    input_list = [preg, glu, bp, skin, insulin, bmi, dpf, age]
    
    prediction = diabetes_model.predict([input_list])
    
    if (prediction[0] == 0):
        return 'The person is not diabetic'
    else:
        return 'The person is diabetic'
    

# New endpoint to check diabetes prediction result
@app.get('/check_diabetes_prediction')
def check_diabetes_prediction():
    # Example input values, you can modify these as needed
    example_input = {
        "pregnancies": 5,
        "Glucose": 120,
        "BloodPressure": 70,
        "SkinThickness": 30,
        "Insulin": 100,
        "BMI": 25.4,
        "DiabetesPedigreeFunction": 0.23,
        "Age": 40
    }
    # Calling the diabetes prediction endpoint to get the result
    result = diabetes_predd(model_input(**example_input))
    return {'prediction_result': result}

# New GET endpoint for checking if the API is running
@app.get('/diabetes_prediction')
def read_root():
    return {'message': 'Diabetes Prediction API is running!'}



