from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import random
from typing import List
import uvicorn
import pandas as pd


app = FastAPI()

class Ingredient(BaseModel):
    name: str
    unit: str
    amount: float

class CookingTimes(BaseModel):
    cooking_time: int
    resting_time: int
    preparation_time: int

class PredictionRequest(BaseModel):
    recipe_text: str
    ingredients: List[Ingredient]

class Feedback(PredictionRequest):
    predicted_times: CookingTimes
    actual_times: CookingTimes

@app.post("/prediction/")
async def predict_cooking_time(prediction_request: PredictionRequest):
    return {
         "cooking_time": random.randint(5,50),
         "resting_time": random.randint(5,50),
         "preparation_time": random.randint(5,50)
    }

@app.post("/feedback/")
async def create_feedback(feedback: Feedback = None):
    df = pd.DataFrame(feedback)
    df.to_csv('csvfile.csv', mode='a', encoding='utf-8', index=False)
    return feedback

@app.get("/")
def read_root():
    return {"Welcome to predictions system"}


### DEBUG
@app.get("/prediction_lite/")
def read_item(ing: Union[str, None]):
    return {"time": random.randint(5,50)}

@app.get("/prediction/")
async def predict_cooking_time(prediction_request: PredictionRequest):
    return {
         "cooking_time": random.randint(5,50),
         "resting_time": random.randint(5,50),
         "preparation_time": random.randint(5,50)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
