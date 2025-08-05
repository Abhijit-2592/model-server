import argparse
import ast
import os
import time
from argparse import RawTextHelpFormatter
from concurrent import futures

import grpc

from . import server_pb2_grpc
from .core import ModelServerServicer, Servable


def _get_custom_servable_class(custom_servable_path):
    with open(custom_servable_path, "r") as f:
        py_file = f.read()
    tree = ast.parse(py_file)
    code = compile(tree, filename=os.path.basename(custom_servable_path), mode="exec")
    namespace = {}
    exec(code, namespace)
    for obj in tree.body:
        if isinstance(obj, ast.ClassDef):
            class_name = obj.name
            if issubclass(namespace[class_name], Servable):
                return namespace[class_name]
    raise ValueError(
        "No custom servable class found! or The custom servable class does not inherit from Servable"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A high performance gRPC server for Machine Learning Models.\n\
Takes in arbitrary optional arguments other than listed below and these are passed to the __init__ method of custom_servable_class",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "custom_servable_path",
        help="Path to the python file containing a custom servable class",
        type=str,
    )
    parser.add_argument(
        "--grpc_port",
        help="Path to config_file used for training. Default 5001",
        type=str,
        metavar="",
        default="5001",
    )

    parser.add_argument(
        "--max_workers",
        help="maximum workers for gRPC server. Default 10",
        type=int,
        metavar="",
        default=10,
    )
    parser.add_argument(
        "--grpc_max_send_message_length",
        help="maximum size of message sent by gRPC server. Def 4MB",
        type=int,
        metavar="",
        default=4 * 1024 * 1024,
    )
    parser.add_argument(
        "--grpc_max_receive_message_length",
        help="maximum size of message sent by gRPC server. Def 4MB",
        type=int,
        metavar="",
        default=4 * 1024 * 1024,
    )

    # Get arbitrary arguments
    parsed, unknown = parser.parse_known_args()
    for arg in unknown:
        if arg.startswith(("-", "--")):
            parser.add_argument(arg, type=str)

    args = parser.parse_args()

    # create a gRPC server
    options = [
        ("grpc.max_send_message_length", args.grpc_max_send_message_length),
        ("grpc.max_receive_message_length", args.grpc_max_receive_message_length),
    ]

    custom_servable_class = _get_custom_servable_class(args.custom_servable_path)
    custom_servable_object = custom_servable_class(args)
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=args.max_workers), options=options
    )

    server_pb2_grpc.add_ModelServerServicer_to_server(
        ModelServerServicer(custom_servable_object=custom_servable_object), server
    )

    print("Starting server. Listening on port {}".format(args.grpc_port))
    server.add_insecure_port("[::]:{}".format(args.grpc_port))
    server.start()

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("\nStopping server!")
        server.stop(0)
