import keras
import numpy as np
from PIL import Image
class ModelTester:
    def __init__(self, config: dict):
        self._config = config
        model_path = self._config.get('model_dir')+"/"+self._config.get("project")
        with open(model_path + "_classes.txt", "r") as file:
            self._classes = file.read().split(",")
        self._model = keras.saving.load_model(model_path+".keras")
    
    def test(self, file_path):
        image_size = self._config.get("dataset").get("image_size")
        img = keras.preprocessing.image.load_img(file_path, target_size=(image_size[0], image_size[1]))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        pred = self._model.predict(img_array)
        print(self._classes[np.argmax(pred)])