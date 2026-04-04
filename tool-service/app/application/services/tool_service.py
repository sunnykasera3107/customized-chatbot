from application.tools.plant_disease_detector import PlantDiseaseDetector
import logging
import os
import requests

class ToolService:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._tool_class_map = {
            'plant_disease_detector': PlantDiseaseDetector
        }

    def handle(self, tool_class_name, image_path):
        path = self._save_file_from_url_(image_path)
        self._logger.info(f"Calling tool: {tool_class_name}")
        tool_class = self._tool_class_map.get(tool_class_name)
        if not tool_class:
            self._logger.error(f"Invalid tool: {tool_class_name}")
            return {"error": f"Invalid tool: {tool_class_name}"}
        
        tool = tool_class('infrastructure/data/model.keras', 'infrastructure/data/classes.txt')
        response = tool.detect(path)
        return response.replace("__", " ").replace("_", " ")
    
    

    def _save_file_from_url_(self, url: str, folder: str = "infrastructure/data/predict"):
        os.makedirs(folder, exist_ok=True)

        filename = url.split("/")[-1] or "downloaded_file"
        file_path = os.path.join(folder, filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return file_path
