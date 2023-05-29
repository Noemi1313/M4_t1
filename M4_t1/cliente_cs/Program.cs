using System.Threading;
using System.Diagnostics;
using Google.Protobuf;
using Grpc.Core;
using RPCClient;
using System;


namespace Application
{
    /// <summary>
    /// Clase principal del programa.
    /// </summary>
    class Program
    {
        /// <summary>
        /// Punto de entrada del programa.
        /// </summary>
        /// <param name="args">Argumentos de línea de comandos.</param>
        static void Main(string[] args)
        {
            // Crear canal gRPC para establecer una conexion con el servidor
            var channel = new Grpc.Core.Channel("127.0.0.1:7042", ChannelCredentials.Insecure);
            // Crear el cliente gRPC 
            var client = new RPC.RPCClient(channel);
            while (true)
            {
                // Hacer una peticion gRPC al servidor para obtener las coordenadas
                var result = client.GetCoord(new Google.Protobuf.WellKnownTypes.Empty());
                // Realizar el display de los valores
                Console.WriteLine("Coordenadas: " + result.Values[0] + ", " + result.Values[1]);
                // Realizar una peticion cada medio segundo
                Thread.Sleep(500);
            }
        }
    }
}
