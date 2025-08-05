import abc
import time

from . import server_pb2_grpc
from .utils import (
    create_array_from_proto,
    create_model_info_proto,
    create_predict_response,
    create_tensor_proto,
    decode_model_info_proto,
)


class Servable(abc.ABC):
    def __init__(self):
        """Abstract base class for custom servables. All custom servables must inherit from this.
        All custom servables inheriting from this must implement the following methods:

        ```python
        predict(self, input_array_dict)
        get_model_info(self, list_of_model_info_dict)
        ```
        """
        pass

    def _get_input_array_dict(self, predict_request_proto):
        input_array_dict = {}
        for key, tensor_proto in predict_request_proto.inputs.items():
            input_array_dict[key] = create_array_from_proto(tensor_proto=tensor_proto)
            self.name = predict_request_proto.name
            self.version = predict_request_proto.version
        input_array_dict["name"] = self.name
        return input_array_dict

    def _make_predict_response(self, output_array_dict):
        tensor_dict = {}
        for key, array in output_array_dict.items():
            tensor_dict[str(key)] = create_tensor_proto(array)
        predict_response = create_predict_response(
            tensor_dict, name=self.name, version=self.version
        )
        return predict_response

    @abc.abstractmethod
    def predict(self, input_array_dict):
        """Abstract method where the model prediction logic lives.
        This method is responsible for the gRPC call GetPredictions().
        All custom servables must define this method.

        Arguments:
            input_array_dict (dict): The PredictionRequest proto decoded as a python dictionary.


        ```python
        # example
        input_array_dict = {
                           "input_tensor_name1": numpy array,
                           "input_tensor_name2": numpy array
                            }
        ```

        Returns:
            A python dictionary with key (typically output name) and value as numpy array of predictions

        ```python
        # example
        output = {
                   "output_tensor_name1": numpy array,
                   "output_tensor_name2": numpy array
                  }
        ```
        """
        pass

    @abc.abstractmethod
    def get_model_info(self, list_of_model_info_dict):
        """Abstract method which is responsible for the call GetModelInfo

        Arguments:
            list_of_model_info_dict (list/tuple): A list containing model_info_dicts

        Note:
            model_info_dict contains the following keys:

            ```python
            {
                "name": "model name as string"
                "version": "version as string"
                "status": "status string"
                "misc": "string with miscellaneous info"
            }
            ```

        Returns:
            list_of_model_info_dict (dict): containing the model and server info. This is similar to the function input
        """
        pass


class ModelServerServicer(server_pb2_grpc.ModelServerServicer):
    def __init__(self, custom_servable_object):
        """gRPC Model Server Services. This is where the RPC methods are defined.

        Arguments:
            custom_servable_object: custom servable classe's instance
        """
        self.custom_servable_object = custom_servable_object

        # Metrics
        self._inference_time = 0

    def GetPredictions(self, request, context):
        """Entrypoint for GetPredictions gRPC call. Uses the predict method defined in custom servable

        Arguments:
            request (protobuf): gRPC request containing input PredictRequest protobuf
            context (protobuf): gRPC context object

        Returns:
            PredictResponse protobuf
        """
        start_time = time.time()
        input_array_dict = self.custom_servable_object._get_input_array_dict(request)
        output_array_dict = self.custom_servable_object.predict(input_array_dict)
        self._inference_time = int(round((time.time() - start_time) * 1e6))
        return self.custom_servable_object._make_predict_response(output_array_dict)

    def GetModelInfo(self, request, context):
        """Entrypoint for GetModelInfo gRPC call. Uses the get_model_info method defined in custom servable

        Arguments:
            request (protobuf): gRPC request containing input ModelInfo protobuf
            context (protobuf): gRPC context object

        Returns:
            ModelInfo protobuf
        """
        request_list_of_model_info_dict = decode_model_info_proto(request)
        response_list_of_model_info_dict = self.custom_servable_object.get_model_info(
            request_list_of_model_info_dict
        )
        return create_model_info_proto(response_list_of_model_info_dict)
