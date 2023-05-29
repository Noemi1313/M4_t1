#!/usr/bin/env python

import grpc
from concurrent import futures
import google.protobuf.empty_pb2 as empty_pb2
import time
import signal
import rpc_pb2_grpc as pb2_grpc

def run():
    # Create a gRPC channel to connect to the server
    channel = grpc.insecure_channel('localhost:7042')  # Replace with the server address and port

    # Create a stub for the gRPC service
    stub = pb2_grpc.RPCStub(channel)

    # Create an empty request message (google.protobuf.Empty)
    request = empty_pb2.Empty()

    # Call the GetCoord RPC method on the server
    response = stub.GetCoord(request)

    # Process the response
    print(response)

if __name__ == '__main__':
    run()
