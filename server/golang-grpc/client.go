package main

import (
	"fmt"

	pb "sampleGRPC"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

var port = ":1112"

func MakeEcho(ctx context.Context, m pb.EchoServiceClient, text string) (*pb.Response, error) {
	request := &pb.Request{
		Message: text,
	}

	r, err := m.Echo(ctx, request)
	if err != nil {
		return nil, err
	}

	return r, nil
}

func main() {
	conn, err := grpc.Dial(port, grpc.WithInsecure())
	if err != nil {
		fmt.Println("dial failed:", err)
		return
	}

	client := pb.NewEchoServiceClient(conn)
	r, err := MakeEcho(context.Background(), client, "echo from CLIENT")
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("Response Text:", r.Message)
}
