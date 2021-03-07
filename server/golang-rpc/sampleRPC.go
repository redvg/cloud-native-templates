package sampleRPC

type Echo struct {
	M string
}

type EchoInterface interface {
	Respond(arguments *Echo, response *string) error
}
