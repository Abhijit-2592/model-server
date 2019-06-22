#!/bin/bash
echo "compiling protobufs!"
protoc --python_out=. model_server/protos/*.proto
protoc --python_out=. model_server/apis/*.proto
# compile gRPC server for python
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. model_server/server.proto
echo "Done!!!"
