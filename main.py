import os
import numpy as np
import json
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from typing import Union
from model import FoodModel
from mongo_connect import connect_mongo

app = FastAPI()

@app.post("/predict")
async def predictas(image: UploadFile):
    contents = await image.read()
    with open(f"uploaded_{image.filename}", "wb") as f:
        f.write(contents)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_file_path = os.path.join(current_dir, "modelFood.h5")
    image_file_path = os.path.join(current_dir, f"uploaded_{image.filename}")
    food_model = FoodModel(model_file_path)
    prediction = food_model.predict(image_file_path)
    top_n = 20
    sorted_indices = np.argsort(prediction)[::-1]
    food_classes = read_food_classes('ClassesName.txt')
    top_predictions = [food_classes[i] for i in sorted_indices[:top_n]]
    return connect_mongo(top_predictions)

def read_food_classes(file_path):
    with open(file_path, 'r') as file:
        food_classes = [line.strip() for line in file]
    return food_classes

@app.get("/images/{image_name}")
async def get_image(image_name: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_dir, "food_image")
    target_dir = os.path.join(image_dir, image_name)
    images = os.listdir(target_dir)
    print(os.path.join(target_dir, images[0]))
    # Return the image file as a response
    return FileResponse(os.path.join(target_dir, images[0]), media_type='image/jpeg')