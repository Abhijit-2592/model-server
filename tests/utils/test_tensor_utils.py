import numpy as np
import pytest

from model_server import utils


def test_creation_and_extraction_of_tensor_proto():
    dtypes = ["float32", "float16", "FLOAT64", "inT32", "UinT8"]
    for dtype in dtypes:
        array = 2.5 * np.random.randn(100, 100, np.random.choice((0, 3))) + 3
        if array.shape[2] == 1:
            array = array.reshape((100, 100))
        my_proto = utils.create_tensor_proto(array, dtype=dtype)
        recreated_array = utils.create_array_from_proto(tensor_proto=my_proto)
        assert np.array_equal(recreated_array, array.astype(dtype.lower()))

    array = np.array(
        ["Test1", "test2", "random stuffs", "This is a string"], dtype=object
    )
    my_proto = utils.create_tensor_proto(array)
    recreated_array = utils.create_array_from_proto(tensor_proto=my_proto)
    assert np.array_equal(recreated_array, np.array([e.encode() for e in array]))

    array = np.array(
        [
            "Test1".encode("utf-8"),
            "test2".encode("utf-8"),
            "random stuffs".encode("utf-8"),
            "This is a string".encode("utf-8"),
        ],
        dtype=object,
    )
    my_proto = utils.create_tensor_proto(array)
    recreated_array = utils.create_array_from_proto(tensor_proto=my_proto)
    assert np.array_equal(recreated_array, array)

    array = np.array(
        ["Test1", "test2", "random stuffs", "This is a string"], dtype=object
    )
    my_proto = utils.create_tensor_proto(array, shape=(2, 2))
    recreated_array = utils.create_array_from_proto(tensor_proto=my_proto)
    assert np.array_equal(
        recreated_array, np.array([e.encode() for e in array]).reshape(2, 2)
    )

    array = np.array(
        ["Test1", "test2", "random stuffs", "This is a string"], dtype=object
    ).reshape((2, 2))
    my_proto = utils.create_tensor_proto(array)
    recreated_array = utils.create_array_from_proto(tensor_proto=my_proto)
    assert np.array_equal(
        recreated_array, np.array([e.encode() for e in array.flatten()]).reshape(2, 2)
    )


if __name__ == "__main__":
    pytest.main([__file__])
