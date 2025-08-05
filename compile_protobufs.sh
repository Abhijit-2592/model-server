#!/bin/bash
set -e

echo "Cleaning up old compiled protobuf files..."
# Find and remove all compiled protobuf files
find . -type f -name "*_pb2.py" -o -name "*_pb2_grpc.py" | xargs rm

echo "compiling protobufs!"
# Find all .proto files and compile them
# print0 is null terminated to handle filenames with spaces
# xargs is used to pass the files to the protoc compiler
# -0 is used to handle null-terminated input
find model_server -name "*.proto" -print0 | xargs -0 python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=.

echo "Done!!!"