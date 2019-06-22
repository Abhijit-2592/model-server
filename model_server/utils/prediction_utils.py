from ..apis import predict_pb2
from ..protos import tensor_pb2


def create_predict_request(input_tensorproto_dict, name=None, version=None):
    """Creates a PredictRequest proto

    Arguments:
        input_tensorproto_dict (dict): A dictionary with key (typically input tensor name string) and value as TensorProto.
        name (str): Optional model name. Default None
        version (str): Optional model version. Default None

    Returns:
        PredictRequest proto
    """
    predict_request = predict_pb2.PredictRequest()
    if name:
        predict_request.name = str(name)
    if version:
        predict_request.version = str(version)
    for key, value in input_tensorproto_dict.items():
        assert isinstance(value, tensor_pb2.TensorProto), "The dictionary must contain TensorProto but got {}".format(type(value))
        assert isinstance(key, str), "They dictionary key must be a string but got {}".format(key)
        predict_request.inputs['{}'.format(key)].CopyFrom(value)
    return predict_request


def create_predict_response(output_tensorproto_dict, name=None, version=None):
    """Creates a PredictResponse proto

    Arguments:
        input_tensorproto_dict (dict): A dictionary with key (typically output tensor name string) and value as TensorProto.
        name (str): Optional model name. Default None
        version (str): Optional model version. Default None

    Returns:
        PredictResponse proto
    """
    predict_response = predict_pb2.PredictResponse()
    if name:
        predict_response.name = str(name)
    if version:
        predict_response.version = str(version)
    for key, value in output_tensorproto_dict.items():
        assert isinstance(value, tensor_pb2.TensorProto), "The dictionary must contain TensorProto but got {}".format(type(value))
        assert isinstance(key, str), "They dictionary key must be a string but got {}".format(key)
        predict_response.outputs['{}'.format(key)].CopyFrom(value)
    return predict_response
