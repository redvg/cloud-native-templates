package main

import (
	"fmt"
	"net"
	pb "sampleGRPC"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

type EchoServer struct{}

var PORT string = ":1112"

func (EchoServer) Echo(ctx context.Context, r *pb.Request) (*pb.Response, error) {
	fmt.Println("got message:", r.Message)

	response := &pb.Response{
		Message: r.Message + " OK!",
	}

	return response, nil
}

func main() {
	server := grpc.NewServer()
	var echoServer EchoServer
	pb.RegisterEchoServiceServer(server, echoServer)
	listen, err := net.Listen("tcp", PORT)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println("Serving requests...")
	server.Serve(listen)
}
