import numpy as np

from model_server import Servable


class my_custom_servable(Servable):
    def __init__(self, args):
        pass

    def predict(self, input_array_dict):
        print(input_array_dict)
        return {
            "output_array": np.array([100, 200]).astype(np.float32),
        }

    def get_model_info(self, list_of_model_info_dict):
        return [
            {"name": "first_model", "version": 1, "status": "up"},
            {"name": "second_model", "version": 2, "status": "down"},
        ]
