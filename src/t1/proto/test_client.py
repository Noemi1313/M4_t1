#!/usr/bin/env python

/**

@file client.py
@brief Cliente gRPC para la solicitud de coordenadas
Implementacion de un cliente gRPC que realiza una solicitud al servidor gRPC
para obtener las coordenadas actuales. Utiliza el paquete rpc_pb2_grpc y google.protobuf.empty_pb2
generados a partir del archivo rpc.proto.
El cliente establece una conexión con el servidor, realiza la solicitud y muestra la respuesta recibida.
El servidor debe estar en ejecución y escuchando en la dirección y puerto especificados.
@author Noemi Carolina Guerra Montiel 
@date Fecha de creación: 29/05/2023
*/

import grpc
from concurrent import futures
import google.protobuf.empty_pb2 as empty_pb2
import time
import signal
import rpc_pb2_grpc as pb2_grpc

def run():
    """
    @brief Función principal del cliente gRPC.
    """
    
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
