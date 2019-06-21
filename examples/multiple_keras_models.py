import tensorflow as tf
import numpy as np
from model_server import Servable


class SessionSafeModel(object):
    def __init__(self, model_loading_function):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.sess = tf.Session()
            with self.sess.as_default():
                self.model = model_loading_function()
                self.model._make_predict_function()


class MultipleModels(Servable):

    def __init__(self, args):
        def func1():
            return tf.keras.applications.InceptionV3(include_top=True, weights="imagenet")

        def func2():
            return tf.keras.applications.VGG16(include_top=True, weights="imagenet")

        self.models_dict = {}
        print("loading InceptionV3")
        self.models_dict["inceptionv3"] = SessionSafeModel(func1)
        print("loading VGG16")
        self.models_dict["vgg16"] = SessionSafeModel(func2)

    def predict(self, input_array_dict):

        image_tensor = input_array_dict["image_tensor"]
        if image_tensor.shape == 3:
            image_tensor = np.expand_dims(image_tensor, axis=0)

        if input_array_dict["name"] == "inceptionv3":
            session_safe_model = self.models_dict["inceptionv3"]
            with session_safe_model.graph.as_default():
                with session_safe_model.sess.as_default():
                    predictions = session_safe_model.model.predict(image_tensor)

        elif input_array_dict["name"] == "vgg16":
            session_safe_model = self.models_dict["vgg16"]
            with session_safe_model.graph.as_default():
                with session_safe_model.sess.as_default():
                    predictions = session_safe_model.model.predict(image_tensor)

        else:
            raise ValueError("Unknown model {}".format(input_array_dict["name"]))
        return {"prediction_scores": predictions}
