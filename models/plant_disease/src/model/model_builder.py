import keras, os
class ModelBuilder:
    def __init__(self, config: dict):
        self._config = config

    def build(self):
        train_ds = self._process_images_()
        class_names = train_ds.class_names
        model = self._prepare_model_(len(class_names))
        self._train_model_(model, train_ds, class_names)
    
    def _train_model_(self, model, dataset, classname):
        training = self._config.get("training")
        model.compile(
            optimizer=training.get("optimizer"),
            loss=training.get("loss"),
            metrics=training.get("metrics")
        )

        model.fit(dataset, epochs=training.get("epochs"))
        model.save(self._config.get("model_dir")+"/"+self._config.get("project")+".keras")
        with open(self._config.get("model_dir")+"/"+self._config.get("project")+"_classes.txt", "w") as file:
            file.write(",".join(classname))

    def _predict_(self, model, file_path):
        pass

    def _prepare_model_(self, num_class): 
        input_shape = self._config.get("model").get("input_shape")
        augmentation = self._config.get("augmentation")
        if augmentation.get("enabled"):
            model = keras.Sequential([
                keras.layers.RandomFlip(augmentation.get("flip")),
                keras.layers.RandomRotation(augmentation.get("rotation")),
                keras.layers.RandomZoom(augmentation.get("zoom")),
                keras.layers.RandomTranslation(height_factor=augmentation.get("height_factor"), width_factor=augmentation.get("width_factor")),
                keras.layers.Rescaling(1./255, input_shape=(input_shape[0], input_shape[1], input_shape[2]))
            ], name="data_augmentation")
        else:
            model = keras.models.Sequential([
                keras.layers.Rescaling(1./255, input_shape=(input_shape[0], input_shape[1], input_shape[2]))
            ])
        kernel_size = self._config.get("model").get("architecture").get("kernel_size")
        max_pooling = self._config.get("model").get("architecture").get("max_pooling")
        for conv_unit in self._config.get("model").get("architecture").get("conv_layers"):
            model.add(
                keras.layers.Conv2D(
                    filters=conv_unit,
                    kernel_size=(kernel_size[0], kernel_size[1]),
                    activation="relu"
                )
            )
            model.add(
                keras.layers.MaxPooling2D(
                    pool_size=(max_pooling[0], max_pooling[1]),
                    padding="same"
                )
            )
        
        model.add(keras.layers.Flatten())
        model.add(
            keras.layers.Dense(self._config.get("model").get("architecture").get("dense_units"), activation="relu")
        )
        model.add(
            keras.layers.Dense(num_class, activation="softmax")
        )

        return model

    def _process_images_(self):
        image_size=self._config.get("dataset").get("image_size")
        train_ds = keras.utils.image_dataset_from_directory(
            self._config.get("data_dir"),
            batch_size=self._config.get("dataset").get("batch_size"),
            image_size=(image_size[0], image_size[1]),
        )
        
        return train_ds