using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Confluent.Kafka;
using Epiphany.Examples.Kafka.Configuration;
using Epiphany.Examples.Messaging;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace Epiphany.Examples.Kafka.Producer
{
    public class KafkaProducer : IProducer
    {
        private readonly ILogger _logger;
        private readonly KafkaConfiguration _defaultConfig;

        public KafkaProducer(IConfiguration configuration, ILogger<KafkaProducer> logger)
        {
            _logger = logger;
            _defaultConfig = new KafkaConfiguration(configuration);
        }

        public Task<bool> Produce(IEnumerable<string> models)
        {
            void Handler(DeliveryReportResult<Null, string> r) => LogDeliveryResult(r);

            using (var p = new Producer<Null, string>(_defaultConfig.ToKafkaProducerConfig()))
            {
                var counter = 0;
                foreach (var model in models)
                {

                    p.BeginProduce(_defaultConfig.TopicName, new Message<Null, string> { Value = model }, Handler);
                    counter++;
                    if (counter > 10) // Flush messages every 10 message
                    {
                        p.Flush(TimeSpan.FromSeconds(10));
                        counter = 0;
                    }
                }
                p.Flush(TimeSpan.FromSeconds(10));
                return Task.FromResult(true);
            }
        }

        private void LogDeliveryResult(DeliveryReportResult<Null, string> deliveryReportResult)
        {
            if (deliveryReportResult.Error.IsError)
            {
                _logger.LogError(deliveryReportResult.Error.Reason);
            }
            else
            {
                _logger.LogInformation($"Delivered message to {deliveryReportResult.TopicPartitionOffset}");
            }
        }
    }
}
