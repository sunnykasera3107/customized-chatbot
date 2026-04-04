import keras
import numpy as np
from PIL import Image
import logging

class PlantDiseaseDetector:
    def __init__(self, model_path: str, class_path: str):
        self._logger = logging.Logger(__name__)
        self._logger.info("Reading model file")
        with open(class_path, "r") as file:
            self._classes = file.read().split(",")
        self._model = keras.saving.load_model(model_path)

    def detect(self, file_path):
        self._logger.info("Predicting plant disease")
        image_size = [192, 192]
        img = keras.preprocessing.image.load_img(file_path, target_size=(image_size[0], image_size[1]))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        pred = self._model.predict(img_array)
        
        return self._classes[np.argmax(pred)]
