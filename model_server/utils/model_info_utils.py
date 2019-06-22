from ..protos import model_info_pb2


def create_model_info_proto(list_of_model_info_dict):
    """Creates a ModelInfo proto

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
        ModelInfo proto

    """
    model_info_proto = model_info_pb2.ModelInfo()
    for model_info_dict in list_of_model_info_dict:
        model_info = model_info_proto.info.add()
        model_info.name = str(model_info_dict.get("name", ""))
        model_info.version = str(model_info_dict.get("version", ""))
        model_info.misc = str(model_info_dict.get("misc", ""))
        model_info.status = str(model_info_dict.get("status", ""))
    return model_info_proto


def decode_model_info_proto(model_info_proto):
    """Decodes the model_info_proto created by create_model_info_proto

    Arguments:
        model_info_proto (ModelInfo proto): model_info_proto created by create_model_info_proto

    Returns:
        list_of_model_info_dict (list): A list containing model_info_dicts

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
    """
    list_of_model_info_dict = []
    for model_info in model_info_proto.info:
        model_info_dict = {}
        model_info_dict["name"] = model_info.name
        model_info_dict["version"] = model_info.version
        model_info_dict["misc"] = model_info.misc
        model_info_dict["status"] = model_info.status
        list_of_model_info_dict.append(model_info_dict)
    return list_of_model_info_dict
