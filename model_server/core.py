import abc
from . import server_pb2_grpc

from .utils import create_tensor_proto, create_array_from_proto
from .utils import create_predict_response
from .utils import decode_model_info_proto, create_model_info_proto


class Servable(abc.ABC):
    def __init__(self):
        pass

    def get_input_array_dict(self, predict_request_proto):
        input_array_dict = {}
        for key, tensor_proto in predict_request_proto.inputs.items():
            input_array_dict[key] = create_array_from_proto(tensor_proto=tensor_proto)
            self.name = predict_request_proto.name
            self.version = predict_request_proto.version
        input_array_dict["name"] = self.name
        return input_array_dict

    def make_predict_response(self, output_array_dict):
        tensor_dict = {}
        for key, array in output_array_dict.items():
            tensor_dict[str(key)] = create_tensor_proto(array)
        predict_response = create_predict_response(tensor_dict, name=self.name, version=self.version)
        return predict_response

    @abc.abstractmethod
    def predict(self, input_array_dict):
        pass

    @abc.abstractmethod
    def model_status(self, list_of_model_info_dict):
        pass


class ModelServerServicer(server_pb2_grpc.ModelServerServicer):
    def __init__(self, custom_servable_object):
        self.custom_servable_object = custom_servable_object

    def GetPredictions(self, request, context):
        input_array_dict = self.custom_servable_object.get_input_array_dict(request)
        output_array_dict = self.custom_servable_object.predict(input_array_dict)
        return self.custom_servable_object.make_predict_response(output_array_dict)

    def GetModelsInfo(self, request, context):
        request_list_of_model_info_dict = decode_model_info_proto(request)
        response_list_of_model_info_dict = self.custom_servable_object.model_status(request_list_of_model_info_dict)
        return create_model_info_proto(response_list_of_model_info_dict)
