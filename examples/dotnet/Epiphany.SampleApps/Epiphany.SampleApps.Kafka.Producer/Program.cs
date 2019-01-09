using Confluent.Kafka;
using Confluent.Kafka.Serialization;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;

namespace Epiphany.KafkaProducer
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
                {"session.timeout.ms", config["KAFKA_SESSION_TIMEOUT_MS"]},
            };

            using (var producer = new Producer<Null, string>(conf, null, new StringSerializer(Encoding.UTF8)))
            {
                for (int i = 0; i < 100; i++)
                {
                    var dr = producer.ProduceAsync("foo", null, RandomString(10)).Result;
                    Console.WriteLine($"Delivered '{dr.Value}' to: {dr.TopicPartitionOffset}");
                }
            }

        }

        private static Random random = new Random();
        public static string RandomString(int length)
        {
            const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
            return new string(Enumerable.Repeat(chars, length)
              .Select(s => s[random.Next(s.Length)]).ToArray());
        }
    }
}
