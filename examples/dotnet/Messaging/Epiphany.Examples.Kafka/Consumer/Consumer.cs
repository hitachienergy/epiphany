using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Confluent.Kafka;
using Confluent.Kafka.Serialization;
using Epiphany.Examples.Kafka.Configuration;
using Epiphany.Examples.Messaging;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace Epiphany.Examples.Kafka.Consumer
{
    public class Consumer : IConsumer
    {
        private readonly ILogger _logger;
        private readonly IMessageHandler _messageHandler;
        private readonly KafkaConfiguration _configuration;

        public Consumer(IConfiguration configuration, ILogger logger, IMessageHandler messageHandler)
        {
            _logger = logger;
            _messageHandler = messageHandler;

            _configuration = new KafkaConfiguration(configuration);
        }
        public Task Consume(CancellationToken cancellationToken)
        {
            using (var consumer = new Consumer<string, string>(_configuration.ToKafkaConfig(), new StringDeserializer(Encoding.UTF8), new StringDeserializer(Encoding.UTF8)))
            {
                //consumer.OnMessage += (_, msg)
                //    => _messageHandler.Handle(msg.Topic, msg.Value);

                consumer.OnError += (_, error)
                    => _logger.LogError($"{error.Code}:{error.Reason}");

                consumer.OnConsumeError += (_, msg)
                    => _logger.LogError($"Consume error: {msg.Error}");

                consumer.Subscribe(_configuration.TopicName);

                while (true)
                {
                    if (cancellationToken.IsCancellationRequested)
                    {
                        return Task.FromResult(1);
                    }
                        
                    if (!consumer.Consume(out Message<string, string> message, 100))
                        continue;
                    _messageHandler.Handle(message.Topic, message.Value);
                }
            }
        }
    }
}
