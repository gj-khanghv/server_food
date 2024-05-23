import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image

class FoodModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
    
    def load_model(self):
        self.model = load_model(self.model_path)
        
        
    def preprocess_image(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))  # Assuming input size is 224x224
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict(self, img_path):
        if self.model is None:
            self.load_model()
        img = self.preprocess_image(img_path)
        prediction = self.model.predict(img)
        return prediction[0]