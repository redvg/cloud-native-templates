package main

import (
	"fmt"
	"net/rpc"
	"os"
	i "sampleRPC"
)

func main() {
	args := os.Args
	if len(args) == 1 {
		fmt.Println("remote host:port string is missing")
		return
	}

	if len(args) == 2 {
		fmt.Println("message is missing")
		return
	}

	REMOTE := args[1]
	c, err := rpc.Dial("tcp", REMOTE)
	if err != nil {
		fmt.Println(err)
		return
	}

	MSG := args[2]
	echoMsg := i.Echo{M: MSG}
	var response string

	err = c.Call("EchoInterface.Respond", echoMsg, &response)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("reply: %s\n", response)
}
