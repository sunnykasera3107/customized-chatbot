import yaml, os, logging
from src.data.data_fetcher import DataFetcher
from src.data.data_cleaner import DataCleaner
from src.model.model_builder import ModelBuilder
from src.model.model_tester import ModelTester

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


def setup_logging():
    if os.getenv("DEBUG_ENABLED", "false").lower() == "true":
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.WARNING,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

# 🔥 Call this ONCE at startup
setup_logging()


def main():
    logger = logging.Logger("Plant Disease")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logger.info(f"Reading configuration file")
    with open(current_dir + "/src/config/config.yaml", "r") as file:
        config = yaml.safe_load(file)


    print(config.get("dataset").get("download"))
    if config.get("dataset").get("download"):
        logger.info(f"Downloading dataset from kaggle")
        dataset = config.get("dataset").get("name")
        raw_data_path = current_dir + '/' + config.get("paths").get("data").get("raw")
        temp_data_path = current_dir + '/' + config.get("paths").get("data").get("temp")
        data_fetcher = DataFetcher(dataset, raw_data_path, temp_data_path)
        data_fetcher.fetch()
    
    # if config.get("dataset").get("process"):
    #     logger.info(f"Cleaning dataset")
    #     raw_data_path = current_dir + '/' + config.get("paths").get("data").get("raw")
    #     processed_data_path = current_dir + '/' + config.get("paths").get("data").get("processed")
    #     data_cleaner = DataCleaner(raw_data_path, processed_data_path)
    #     data_cleaner.clean()

    model_config = {
        'data_dir': current_dir + "/" + config.get("paths").get("data").get("raw") + "/PlantVillage",
        'model_dir': current_dir + "/" + config.get("paths").get("models").get("save_dir"),
        'project': config.get("project").get("name"),
        'dataset': config.get("dataset"),
        'training': config.get("training"),
        'model': config.get("model"),
        'augmentation': config.get("augmentation")
    }

    if config.get("model").get("building"):
        model_builder = ModelBuilder(model_config)
        model_builder.build()

    if config.get("model").get("testing"):
        model_tester = ModelTester(model_config)
        test_path = current_dir + "/" + config.get("paths").get("data").get("test")
        for file in os.listdir(test_path):
            file_path = os.path.join(test_path, file)
            model_tester.test(file_path)


if __name__ == "__main__":
    main()