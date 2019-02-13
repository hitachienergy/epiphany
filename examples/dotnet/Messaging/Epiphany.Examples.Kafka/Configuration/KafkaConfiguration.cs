using Confluent.Kafka;
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.Kafka.Configuration
{
    public class KafkaConfiguration
    {
        public string TopicName { get; set; }
        public string BootstrapServers { get; set; }
        public string KafkaGroupId { get; set; }
        public int SessionTimeout { get; set; }
        public KafkaConfiguration(IConfiguration configuration)
        {
            TopicName = configuration["TOPIC_NAME"];
            KafkaGroupId = configuration["KAFKA_GROUP_ID"];
            BootstrapServers = configuration["KAFKA_ENDPOINT"];
            SessionTimeout = int.Parse(configuration["KAFKA_SESSION_TIMEOUT_MS"]);
        }

        public ProducerConfig ToKafkaProducerConfig()
        {
            return new ProducerConfig
            {
                BootstrapServers = BootstrapServers,
                GroupId = KafkaGroupId,
                SessionTimeoutMs = SessionTimeout
            };
        }
        public ConsumerConfig ToKafkaConsumerConfig()
        {
            return new ConsumerConfig
            {
                BootstrapServers = BootstrapServers,
                GroupId = KafkaGroupId,
                AutoOffsetReset = AutoOffsetResetType.Earliest,
                SessionTimeoutMs = SessionTimeout
            };
        }
    }
}
