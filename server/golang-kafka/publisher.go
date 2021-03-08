package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/segmentio/kafka-go"
	"math/rand"
	"os"
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
	conn, err := kafka.DialLeader(context.Background(), "tcp", remote, topic, partition)
	if err != nil {
		fmt.Printf("%s\n", err)
		return
	}

	rand.Seed(time.Now().Unix())
	count := 10

	for i := 0; i < count; i++ {
		somerand := rand.Intn(123)
		temp := Record{somerand}
		recordJSON, _ := json.Marshal(temp)

		conn.SetWriteDeadline(time.Now().Add(1 * time.Second))
		conn.WriteMessages(
			kafka.Message{Value: []byte(recordJSON)},
		)

		time.Sleep(10 * time.Millisecond)
	}

	fmt.Println()
	conn.Close()
}
