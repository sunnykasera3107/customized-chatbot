import kagglehub, os, shutil, logging

class DataFetcher:
    def __init__(self, dataset: str, download_path: str, temp_dir: str):
        self._logger = logging.Logger("Model Builder")
        self._dataset = dataset
        self._download_path = download_path
        self._temp_dir = temp_dir

    def fetch(self):
        self._logger.info(f"Downloading dataset from kaggle")
        path = kagglehub.dataset_download(self._dataset, output_dir=self._temp_dir)

        if not os.path.exists(self._download_path):
            self._logger.info(f"Creating download path folder")
            os.makedirs(self._download_path)
        
        self._logger.info(f"Moving all files from downloaded kaggle path to raw file path.")
        for file in os.listdir(path):
            shutil.move(os.path.join(path, file), self._download_path)