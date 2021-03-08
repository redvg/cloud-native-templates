package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	"github.com/segmentio/kafka-go"
)

type Record struct {
	Random int `json:"random"`
}

func main() {
	topic := ""
	if len(os.Args) > 1 {
		topic = os.Args[1]
	} else {
		fmt.Println("Usage:", os.Args[0], "TOPIC")
		return
	}

	partition := 0
	remote := "localhost:9092"

	r := kafka.NewReader(kafka.ReaderConfig{
		Brokers:   []string{remote},
		Topic:     topic,
		Partition: partition,
		MinBytes:  10e3,
		MaxBytes:  10e6,
	})
	r.SetOffset(0)

	for {
		m, err := r.ReadMessage(context.Background())
		if err != nil {
			break
		}
		fmt.Printf("message at offset %d: %s = %s\n", m.Offset, string(m.Key), string(m.Value))

		temp := Record{}
		err = json.Unmarshal(m.Value, &temp)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Printf("%T\n", temp)
	}

	r.Close()
}
