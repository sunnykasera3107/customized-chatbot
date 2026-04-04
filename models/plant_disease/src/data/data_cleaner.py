import os, shutil, logging

class DataCleaner:
    def __init__(self, raw_path, processed_path):
        self._logger = logging.Logger("Plant Disease")
        self._raw_path = raw_path
        self._processed_path = processed_path

    def clean(self):
        if not os.path.exists(self._raw_path):
            self._logger.error(f"No data found at {self._raw_path}")
            return {"error": f"No data found at {self._raw_path}"}
        
        if not os.path.exists(self._processed_path):
            self._logger.info(f"Creating dir: {self._processed_path}")
            os.mkdir(self._processed_path)

        self._fetch_inner_dir_files_(self._raw_path, self._processed_path)

    
    def _fetch_inner_dir_files_(self, path: str, processed_path: str):
        for root, dirs, files in os.walk(self._raw_path):
            if len(files) > 0:
                for file in files:
                    label = os.path.basename(root)
                    label_dir = os.path.join(processed_path, label)
                    os.makedirs(label_dir, exist_ok=True)
                    src = os.path.join(root, file)                    
                    dst = os.path.join(label_dir, file)
                    shutil.copy(src, dst)
