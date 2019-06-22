# examples
examples to use `Model Server`.

Each folder contains a `python` file which contains a `custom_servable` and a `Jupyter Notebook` containing the client

-   [images](./images): folder containing images used by examples. This folder is tracked with `GIT LFS`

-   [simple_servable](./simple_servable): Contains a very minimalistic example to use `Model Server`

    **Usage:**
    ```bash
    python -m model_server.runserver examples/simple_servable/simple_servable.py
    ```

-   [keras_image_classification](./keras_image_classification): contains a simple keras based custom servable for image classification using **Inception-V3** pretrained on imagenet

    **Usage:**
    ```bash
    python -m model_server.runserver examples/keras_image_classification/keras_image_classification.py
    ```
-   [multiple_keras_models](./multiple_keras_models): Contains an example which hosts both `VGG16` and
`Inception-V3` in Keras

    **Usage:**
    ```bash
    python -m model_server.runserver examples/multiple_keras_models/multiple_keras_models.py
    ```
