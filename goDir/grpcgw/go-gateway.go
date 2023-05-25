package main

import(
	"context"
	"flag"
	"fmt"
	"net/http"
	"github.com/golang/glog"
	"google.golang.org/grpc"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	gw "rpc-gw.com/rest-gw/proto"
)

var (
	grpcServerEndpoint = flag.String("grpc-server-endpoint", "127.0.0.1:7042", "gRPC svr endpoint")
	gw_port = "8042"
)

func run() error{
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	mux := runtime.NewServerMux()
	opts := []grpc.DialOption(grpc.WithInsecure())
	err := gw.RegisterRPCDemoHandleFromEndpoint(ctx, mux, *grpcServerEndpoint, opts)
	if err != nil{
		return err
	}

	return http.listenAndServe(":"+gw_port, mux)
}

func main(){
	flag Parse()
	defer.glog.Flush()
	fmt.Println("Starting Gateway at " + gw_port)
	if err := run(); err != nil{
		glog.Fatal(err)
	}
}