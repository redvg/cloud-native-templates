```bash
mkdir -p $GOPATH/src/sampleRPC
cp sampleRPC.go $GOPATH/src/sampleRPC/
go install sampleRPC
go run server.go
go run client.go localhost:1111 foo
```
this yields `reply: got foo`
