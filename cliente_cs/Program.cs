using System.Threading;
using System.Diagnostics;
using Google.Protobuf;
using Grpc.Core;
using RPCClient;
using System;


namespace Application
{
    class Program
    {
        static void Main(string[] args)
        {
            var channel = new Grpc.Core.Channel("127.0.0.1:7042", ChannelCredentials.Insecure);
            var client = new RPC.RPCClient(channel);
            while (true)
            {
                var result = client.GetCoord(new Google.Protobuf.WellKnownTypes.Empty());
                Console.WriteLine("Coordenadas: " + result.Values[0] + ", " + result.Values[1]);
                Thread.Sleep(500);
            }
        }
    }
}