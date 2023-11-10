# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:14:44 2022

@author: siddhardhan
"""


import json
import requests


url = 'https://3892-35-185-84-213.ngrok.io/diabetes_prediction'

input_data_for_model = {
    
    'Pregnancies' : 5,
    'Glucose' : 120,
    'BloodPressure' : 70,
    'SkinThickness' : 30,
    'Insulin' : 100,
    'BMI' : 25.4,
    'DiabetesPedigreeFunction' : 0.23,
    'Age' : 40
    
    }

input_json = json.dumps(input_data_for_model)

response = requests.post(url, data=input_json)
# response = requests.get(url, data=input_json)


print(response.text)


