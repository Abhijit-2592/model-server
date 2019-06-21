import numpy as np
from model_server import Servable


class my_custom_servable(Servable):
    def __init__(self, args):
        print(args.check)

    def predict(self, input_array_dict):
        print(input_array_dict)
        return ({"output_array": np.array([100, 200]).astype(np.float32),
                 })
