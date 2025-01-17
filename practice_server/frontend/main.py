from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import numpy as np
import pandas as pd

app = FastAPI()

@app.get("/greeting")
def root_index():
    return {
        "message": "안녕하세요"
    }

@app.post("/predict")
def predict_ml(x: str):
    return {
        "x": x,
        "message": f"{x} 안녕하세요"
    }

@app.post("/sum")
def predict_ml(x1: int, x2: int):
    return {
        "message": "더하기 결과입니다.",
        "result": x1 + x2
    }

model_path = "titanic_model.pkl"
model = joblib.load(model_path)

class TitanicRequest(BaseModel):
    Pclass: int
    Sex: int  # 0: female, 1: male
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: int  # 0, 1, 2

@app.post("/titanic/predict")
def predict_titanic(request: TitanicRequest):
    print("등급은", request.Pclass)
    print("성별은", request.Sex)
    input_data = np.array([[feature[1] for feature in [*request]]])
    print(input_data)
    pred = model.predict(input_data)
    if pred[0] == 1:
        return "생존"
    else:
        return "사망"



# uvicorn main:app --reload
