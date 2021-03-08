package main

import (
	"log"
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	counterOfPings := promauto.NewCounter(prometheus.CounterOpts{
		Name: "foo_pings_total",
		Help: "Count of pings",
	})

	http.Handle("/metrics", promhttp.Handler())

	http.Handle("/ping", http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		counterOfPings.Inc()
		_, _ = w.Write([]byte("got ping!\n"))
	}))

	log.Println("serving http://localhost:8080/metrics for prometheus scraper")
	log.Println("hit localhost:8080/ping to generate data")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
