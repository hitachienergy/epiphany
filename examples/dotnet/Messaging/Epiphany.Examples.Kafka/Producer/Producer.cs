using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using Confluent.Kafka;
using Confluent.Kafka.Serialization;
using Epiphany.Examples.Kafka.Configuration;
using Epiphany.Examples.Messaging;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace Epiphany.Examples.Kafka.Producer
{
    public class Producer : IProducer
    {
        private readonly ILogger _logger;

        public Producer(IConfiguration configuration, ILogger logger)
        {
            _logger = logger;
            _defaultConfig = new KafkaConfiguration(configuration);
        }

        private readonly KafkaConfiguration _defaultConfig;

        public async Task<bool> Produce(IEnumerable<string> models)
        {
            using (var producer = new Producer<Null, string>(_defaultConfig.ToKafkaConfig(), null, new StringSerializer(Encoding.UTF8)))
            {
                foreach (var generatedModel in models)
                {
                    var result = await producer.ProduceAsync(_defaultConfig.TopicName, null, generatedModel);
                    if (result.Error.HasError)
                    {
                        _logger.LogError(result.Error.ToString());
                        return await Task.FromResult(false);
                    }
                }

                return await Task.FromResult(true);
            }
        }
    }
}
