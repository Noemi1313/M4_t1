#!/usr/bin/env python
/**

@file server.py
@brief Servidor gRPC para la transmisión de coordenadas
Implementacion un servidor gRPC que se suscribe a un tópico de ROS
para recibir coordenadas y proporcionarlas a los clientes gRPC que realicen
la solicitud correspondiente. Utiliza el paquete rpc_pb2 y rpc_pb2_grpc
generados a partir del archivo rpc.proto.
@author Noemi Carolina Guerra Montiel
@date Fecha de creación: 29/05/2023
*/

# Servidor gRPC
# Noemi Carolina Guerra Montiel - A00826944

# Librerias ROS
import rospy
from std_msgs.msg import Float64MultiArray
# Librerias gRPC
import grpc
from concurrent import futures
import signal
import threading
import rpc_pb2_grpc as pb2_grpc
import rpc_pb2 as pb2


class RPCService(pb2_grpc.RPCServicer):
    """
    @class RPCService
    @brief Clase que implementa el servicio gRPC y sus operaciones.
    """

    def __init__(self, *args, **kwargs):
        """
        @brief Inicializa la clase RPCService.
        @param args Argumentos posicionales adicionales.
        @param kwargs Argumentos de palabras clave adicionales.
        """
        self.data = [0, 0, 0]
        # Suscribirse al topico de las coordenadas
        rospy.Subscriber('/coord', Float64MultiArray, self.UpdateData)

    # Callback del topico de las coordenadas
    def UpdateData(self, data):
        """
        @brief Actualiza los datos de las coordenadas cuando se recibe una actualización del tópico.
        @param data Datos recibidos del tópico de ROS.
        """
        self.data[0] = data.data[0]
        self.data[1] = data.data[1]
        self.data[2] = data.data[2]

    # Pasar las coordenadas
    def GetCoord(self, request, context):
        """
        @brief Implementa la operación GetCoord del servicio RPC.
        @param request Objeto de solicitud de gRPC.
        @param context Contexto de la solicitud.
        @return Objeto de respuesta de gRPC que contiene las coordenadas actuales.
        """
        results = pb2.Coords()
        results.values.append(self.data[0])
        results.values.append(self.data[1])
        results.values.append(self.data[2])
        print("Inicializando...")
        return results

# Salir
def terminate_server(signum, frame):
    """
    @brief Manejador de señal para finalizar el servidor.
    @param signum Número de señal.
    @param frame Marco de la señal.
    """
    print("Got Signal: ", frame)
    rospy.signal_shutdown("Ending rosnode")
    terminate.set()
            
if __name__ == '__main__':
    # Crear un evento para terminar el server
    terminate = threading.Event()
    # Hacer que el server acabe con SIGINT o ctrl+c
    signal.signal(signal.SIGINT, terminate_server)
    # Inicializar el nodo de ROS
    rospy.init_node('wrapper', anonymous=True)

    print("Start sever")
    # Definir la direccion del servidor
    addr = "[::]:7042"
    # Crear una instancia de la clase RPCService
    service =RPCService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Anadir la implementacion del servicio rpc al servidor
    pb2_grpc.add_RPCServicer_to_server(service, server)
    # Anadir el puerto previamente declarado
    server.add_insecure_port(addr)
    # Iniciar el servidor
    server.start()
    print("Server started and listening on [::]:7042")

    rospy.spin()
    print("Exit")
    # Esperar a que se de la llamada de terminacion del servicio
    terminate.wait()
    # Detener el servicio
    server.stop(1).wait()
    





