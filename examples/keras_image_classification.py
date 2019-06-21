import tensorflow as tf
import numpy as np
from model_server import Servable


class InceptionV3Classifier(Servable):
    def __init__(self, args):
        print("Loading InceptionV3 from tf.keras")
        self.model = tf.keras.applications.InceptionV3(include_top=True, weights="imagenet")
        # This is a hack to make this work with server. Check https://github.com/keras-team/keras/issues/2397
        # If you don't run this, you will get <tensor> is not an element of this graph error
        self.model._make_predict_function()
        print("Model loaded!")

    def predict(self, input_array_dict):
        image_tensor = input_array_dict["image_tensor"]
        if image_tensor.shape == 3:
            image_tensor = np.expand_dims(image_tensor, axis=0)
        predictions = self.model.predict(image_tensor)
        return {"prediction_scores": predictions}
