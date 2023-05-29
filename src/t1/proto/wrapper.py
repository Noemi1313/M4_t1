#!/usr/bin/env python
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

    def __init__(self, *args, **kwargs):
        self.data = [0, 0, 0]
        # Suscribirse al topico de las coordenadas
        rospy.Subscriber('/coord', Float64MultiArray, self.UpdateData)

    # Callback del topico de las coordenadas
    def UpdateData(self, data):
        self.data[0] = data.data[0]
        self.data[1] = data.data[1]
        self.data[2] = data.data[2]

    # Pasar las coordenadas
    def GetCoord(self, request, context):
        results = pb2.Coords()
        results.values.append(self.data[0])
        results.values.append(self.data[1])
        results.values.append(self.data[2])
        print("Inicializando...")
        return results

# Salir
def terminate_server(signum, frame):
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
    





