#!/bin/bash
protoc --python_out=. model_server/protos/*.proto
protoc --python_out=. model_server/apis/*.proto
# compile gRPC server for python
python -m grpc_tools.protoc -I=model_server --python_out=. --grpc_python_out=. model_server/server.proto
