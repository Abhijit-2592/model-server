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

    def model_status(self, list_of_model_info_dict):
        if len(list_of_model_info_dict) == 0:
            return [{"name": "InceptionV3", "version": 1, "status": "up", "misc": "This is a test"},
                    {"name": "VGG16", "version": 1, "status": "up", "misc": "This is a test"}
                    ]
        else:
            response_list = []
            for model_info_dict in list_of_model_info_dict:
                response_model_info_dict = {}
                name = model_info_dict.get("name", "")
                if name not in self.models_dict.keys():
                    response_model_info_dict["name"] = name
                    response_model_info_dict["status"] = "UNKNOWN MODEL"
                    response_model_info_dict["misc"] = "MODEL NOT IN SERVER"
                else:
                    response_model_info_dict["name"] = name
                    response_model_info_dict["status"] = "up"
                    response_model_info_dict["misc"] = "This is a test"
                    response_model_info_dict["version"] = 1

                response_list.append(response_model_info_dict)
            return response_list
