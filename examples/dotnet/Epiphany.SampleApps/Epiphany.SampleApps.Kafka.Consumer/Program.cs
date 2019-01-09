using Confluent.Kafka;
using Confluent.Kafka.Serialization;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Text;

namespace Epiphany.KafkaConsumer
{
    class Program
    {
        static void Main(string[] args)
        {
            IConfiguration config = new ConfigurationBuilder()
                .AddEnvironmentVariables()
                .Build();

            var conf = new Dictionary<string, object>
            {
                { "group.id", config["KAFKA_GROUP_ID"] },
                { "bootstrap.servers", config["KAFKA_BOOTSTRAP_SERVERS"]},
                { "auto.commit.interval.ms", config["KAFKA_AUTO_COMMIT_INVETRVAL_MS"] },
                { "auto.offset.reset", config["KAFKA_AUTO_OFFSET_RESET"]},
                { "session.timeout.ms", config["KAFKA_SESSION_TIMEOUT_MS"]},
            };


            using (var consumer = new Consumer<string, string>(conf, new StringDeserializer(Encoding.UTF8), new StringDeserializer(Encoding.UTF8)))
            {
                consumer.OnMessage += (_, msg)
                  => Console.WriteLine($"Read '{msg.Value}' from: {msg.TopicPartitionOffset}");

                consumer.OnError += (_, error)
                  => Console.WriteLine($"Error: {error}");

                consumer.OnConsumeError += (_, msg)
                  => Console.WriteLine($"Consume error ({msg.TopicPartitionOffset}): {msg.Error}");

                consumer.Subscribe("foo");

                while (true)
                {
                    consumer.Poll(TimeSpan.FromMilliseconds(100));
                }
            }
        }
    }
}
