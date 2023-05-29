package main

import(
	"context"
	"flag"
	"fmt"
	"net/http"
	"github.com/golang/glog"
	"google.golang.org/grpc"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	gw "rest-gw.com/rest-gw/proto"
)

var (
	grpcServerEndpoint = flag.String("grpc-server-endpoint", "127.0.0.1:7042", "gRPC svr endpoint")
	gw_port = "8042"
)

/**
 * @brief Ejecuta el servidor gateway que enruta las solicitudes HTTP a gRPC.
 * @return Error en caso de haber ocurrido un problema, o nil si se ejecutó correctamente.
 */

func run() error{
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithInsecure()}
	err := gw.RegisterRPCHandlerFromEndpoint(ctx, mux, *grpcServerEndpoint, opts)
	if err != nil{
		return err
	}

	return http.ListenAndServe(":"+gw_port, mux)
}

func main(){
	flag.Parse()
	defer glog.Flush()
	fmt.Println("Starting Gateway at " + gw_port)
	if err := run(); err != nil{
		glog.Fatal(err)
	}
}