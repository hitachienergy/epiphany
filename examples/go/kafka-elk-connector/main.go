package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"encoding/json"
	"strings"
	"sync"

	kafka "github.com/segmentio/kafka-go"
	elasticsearch "github.com/elastic/go-elasticsearch/v6"
	"github.com/elastic/go-elasticsearch/v6/esapi"
)

func getKafkaReader(kafkaURL, topic, groupID string) *kafka.Reader {
	return kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{kafkaURL},
		GroupID:  groupID,
		Topic:    topic,
		MinBytes: 10, // 10KB
		MaxBytes: 10e6, // 10MB
	})
}

func main() {

	// get parameters from environment variables.
	kafkaURL := os.Getenv("KAFKA_URL")
	topic := os.Getenv("TOPIC")
	groupID := os.Getenv("GROUP_ID")
	elasticUrl := os.Getenv("ELASTIC_URL")
	elkIndexName := os.Getenv("INDEX_NAME")

	es, err := elasticsearch.NewDefaultClient()

	var (
		r  map[string]interface{}
		wg sync.WaitGroup
	  )


	if err != nil {
		log.Fatalf("Error creating the client: %s", err)
	  }
	
	  res, err := es.Info()
	  if err != nil {
		log.Fatalf("Error getting response: %s", err)
	  }
	  // Check response status
	  if res.IsError() {
		log.Fatalf("Error: %s", res.String())
	  }
	  // Deserialize the response into a map.
	  if err := json.NewDecoder(res.Body).Decode(&r); err != nil {
		log.Fatalf("Error parsing the response body: %s", err)
	  }
	  // Print client and server version numbers.
	  log.Printf("Client: %s \n Server: %s", elasticsearch.Version, r["version"].(map[string]interface{})["number"])

	reader := getKafkaReader(kafkaURL, topic, groupID)

	defer reader.Close()

	fmt.Printf("Start consuming Kafka: %s topic: %s, consumer group: %s, and pass to to ELK: %s, index: %s \n", kafkaURL, topic, groupID, elasticUrl, elkIndexName)
	counter := 0
	for {
		m, err := reader.ReadMessage(context.Background())
		if err != nil {
			log.Fatalln(err)
		}
		
		// simply skip messages if there are different type then data
		messageStr := string(m.Value)
		if (strings.Contains(messageStr, "alarm\":") || strings.Contains(messageStr, "event\":")){
			
			continue
		}

		wg.Add(1)
	
		go func(msgData string) {
		  defer wg.Done()
	
		  // Set up the request object directly.
		  req := esapi.IndexRequest{
			Index:      elkIndexName,
			Body:       strings.NewReader(msgData),
			Refresh:    "true",
		  }
	
		  // Perform the request with the client.
		  res, err := req.Do(context.Background(), es)
		  if err != nil {
			log.Fatalf("Error getting response: %s", err)
		  }
		  defer res.Body.Close()
	
		  if res.IsError() {
			log.Printf("[%s] Error indexing object: \n %s", res.Status(), msgData)
		  } else {
			var r map[string]interface{}
			if err := json.NewDecoder(res.Body).Decode(&r); err != nil {
			  log.Printf("Error parsing the response body: %s", err)
			} else {
			  log.Printf("[%s] %s; version=%d", res.Status(), r["result"], int(r["_version"].(float64)))
			}
		  }
		}(messageStr)
	
	  // write to Elastic every 10 messages
	  if (counter > 10){
		  wg.Wait()
		  counter = 0
	  }
	  counter = counter + 1
	}
}