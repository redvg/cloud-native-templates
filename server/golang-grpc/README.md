```bash
brew install protobuf
go get -u github.com/golang/protobuf/protoc-gen-go
cd proto
protoc -I . --go_out=plugins=grpc:. api.proto
```
