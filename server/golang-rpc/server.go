package main

import (
	"fmt"
	"net"
	"net/rpc"
	"os"
	i "sampleRPC"
)

type EchoInterface struct{}

var PORT = ":1111"

func (t *EchoInterface) Respond(arguments *i.Echo, response *string) error {
	*response = "got: " + arguments.M
	return nil
}

func main() {
	args := os.Args
	if len(args) != 1 {
		PORT = ":" + args[1]
	}

	echoInterface := new(EchoInterface)
	rpc.Register(echoInterface)
	t, err := net.ResolveTCPAddr("tcp4", PORT)
	if err != nil {
		fmt.Println(err)
		return
	}
	l, err := net.ListenTCP("tcp4", t)
	if err != nil {
		fmt.Println(err)
		return
	}

	for {
		c, err := l.Accept()
		if err != nil {
			continue
		}
		fmt.Printf("%s\n", c.RemoteAddr())
		rpc.ServeConn(c)
	}
}
