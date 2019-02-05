using System.Collections.Generic;
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.Kafka.Configuration
{
    public class KafkaConfiguration
    {
        public string TopicName { get; set; }
        public string BootstrapServers { get; set; }
        public string KafkaGroupId { get; set; }
        public int KafkaCommitInterval { get; set; }
        public int OffsetReset { get; set; }
        public int SessionTimeout { get; set; }
        public KafkaConfiguration(IConfiguration configuration)
        {
            TopicName = configuration["TOPIC_NAME"];
            KafkaGroupId = configuration["KAFKA_GROUP_ID"];
            BootstrapServers = configuration["KAFKA_ENDPOINT"];
            KafkaCommitInterval = int.Parse(configuration["KAFKA_AUTO_COMMIT_INTERVAL_MS"]);
            OffsetReset = int.Parse(configuration["KAFKA_AUTO_OFFSET_RESET"]);
            SessionTimeout = int.Parse(configuration["KAFKA_SESSION_TIMEOUT_MS"]);
        }

        public Dictionary<string, object> ToKafkaConfig()
        {
            return new Dictionary<string, object>
            {
                { "group.id", KafkaGroupId },
                { "bootstrap.servers", BootstrapServers},
                { "auto.commit.interval.ms", KafkaCommitInterval },
                { "auto.offset.reset", OffsetReset},
                { "session.timeout.ms", SessionTimeout},
            };
        }
    }
}
