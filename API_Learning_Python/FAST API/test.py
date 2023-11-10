
from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def Home(): 
    return {"data":"Test"}