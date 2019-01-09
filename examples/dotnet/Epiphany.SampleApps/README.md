# Epiphany examples .NET Core 2.1

## Kafka
This readme is targeted towards developers, who want to see an example of how to use kafka.

For .NET Core app we advise using the following

* https://github.com/confluentinc/confluent-kafka-dotnet (https://www.nuget.org/packages/Confluent.Kafka/)

### Example.Kafka.WebProducer

This is a sample application that takes a POST request to /api/kafka with the follwing json

```json
{
    "topic": "foo",
    "message": "sdfgsdfgsdfgsdfgsdfgsdfgsdfg"
}
```

with headers:

```text
Content-Type: application/json
```

And the message should be put into the queue. (1 message per queue)


### Example.KafkaProducer

Simple implementation that puts 100 random messages into queue on topic ```foo```

### Example.KafkaConsumer

Simple implementation that puts messages from the queue onto stdout.

### Caveats

1. Copy over part of /etc/hosts with public IPs from kafka Server to your PC (example. In Windows /etc/hosts are located in ```C:\Windows\System32\drivers\etc\hosts```. You need to edit them as Administrator

```text
# Public IPs
40.67.255.155  epidevk8s-001  epidevk8s-001-public
40.67.253.172  epidevk8s-002  epidevk8s-002-public
40.67.253.223  epidevk8s-003  epidevk8s-003-public
```

 NOTE: this is just an example file, yours will differ