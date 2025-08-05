import numpy as np
import pytest

from model_server import utils


def test_create_predict_request():
    array = 2.5 * np.random.randn(100, 100, 3) + 3
    array = array.astype(np.float32)
    tensor_proto = utils.create_tensor_proto(array)
    request_proto = utils.create_predict_request({"some_name": tensor_proto})
    assert np.array_equal(
        utils.create_array_from_proto(tensor_proto=request_proto.inputs["some_name"]),
        array,
    )


def test_create_predict_response():
    array = 2.5 * np.random.randn(100, 100, 3) + 3
    array = array.astype(np.float32)
    tensor_proto = utils.create_tensor_proto(array)
    response_proto = utils.create_predict_response({"some_name": tensor_proto})
    assert np.array_equal(
        utils.create_array_from_proto(tensor_proto=response_proto.outputs["some_name"]),
        array,
    )


if __name__ == "__main__":
    pytest.main([__file__])
