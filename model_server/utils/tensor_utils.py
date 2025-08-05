import numpy as np

from ..protos import tensor_pb2


def create_tensor_proto(array, shape=None, dtype=None, name=None):
    """Create a TensorProto from numpy array.

    Arguments:
        array (np.ndarray): The numpy array to convert to TensorProto
        shape (tuple): Optional shape of the array to reshape it to.
            If not given, it is inferred from the numpy array. Default None
        dtype (str): Optional dtype to convert the array to.
            Refer tensor.proto for supported datatypes.
            If not given, it is inferred from the numpy array. Default None.
        name (str): Optional name for the TensorProto. Default None

    Returns:
        A TensorProto containing the given array

    Note:
        - python strings will be encoded to python bytes.
        - Use dtype = "object" if the numpy array contains strings.
        - dtype "string" and "object" are treated as same.
        - "string" is converted to python "object". This is because,
        numpy handles variable length strings in this way
    """
    if not isinstance(array, np.ndarray):
        raise TypeError(
            "array must be of type np.ndarray but, got {}".format(type(array))
        )
    if not shape:
        shape = array.shape
    else:
        array = array.reshape(shape)

    if not dtype:
        dtype = str(array.dtype)
    else:
        dtype = dtype.lower()
        array = array.astype(np.dtype(dtype))

    if dtype.upper() not in tensor_pb2.DType.keys():
        raise TypeError(
            "Only {} datatypes are supported. But got a datatype {}".format(
                tensor_pb2.DType.keys(), dtype.upper()
            )
        )

    # {"float32":0, "uint8": 4} etc
    dtype_dict = {
        k.lower(): v for k, v in zip(tensor_pb2.DType.keys(), tensor_pb2.DType.values())
    }
    tensor_proto = tensor_pb2.TensorProto()
    for dim in shape:
        tensor_shape = tensor_proto.tensor_shape.add()
        tensor_shape.size = dim
    if dtype not in ["string", "object"]:
        tensor_proto.tensor_content = array.tobytes()
    else:
        string_list = []
        for string_val in array.flatten():
            if isinstance(string_val, str):
                string_list.append(string_val.encode("utf-8"))
            elif isinstance(string_val, bytes):
                string_list.append(string_val)
            else:
                raise TypeError(
                    "string elements in array must be of type str or bytes but got {}".format(
                        type(string_val)
                    )
                )

        tensor_proto.string_val.extend(string_list)
    if name:
        tensor_proto.name = str(name)
    tensor_proto.dtype = dtype_dict[dtype]
    return tensor_proto


def create_array_from_proto(tensor_proto):
    """Retrive array from TensorProto.

    Arguments:
        tensor_proto (TensorProto): An instance of TensorProto

    Returns:
        numpy array

    Note:
        - python strings will be encoded to python bytes.
        - Use dtype = "object" if the numpy array contains strings.
        - dtype "string" and "object" are treated as same.
        - "string" is converted to python "object". This is because,
        numpy handles variable length strings in this way
    """
    if not isinstance(tensor_proto, tensor_pb2.TensorProto):
        raise TypeError(
            "tensor_proto must be a TensorProto but got {}".format(type(tensor_proto))
        )
    shape = [d.size for d in tensor_proto.tensor_shape]
    dtype_reversed_dict = {
        v: k.lower() for k, v in zip(tensor_pb2.DType.keys(), tensor_pb2.DType.values())
    }
    dtype = dtype_reversed_dict[int(tensor_proto.dtype)]
    if dtype not in ["string", "object"]:
        array = np.frombuffer(
            tensor_proto.tensor_content, dtype=np.dtype(dtype)
        ).reshape(shape)
    else:
        if dtype == "string":
            dtype = "object"
        array = np.array(tensor_proto.string_val, dtype=object).reshape(shape)

    return array
