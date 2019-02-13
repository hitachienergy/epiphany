using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Confluent.Kafka;
using Epiphany.Examples.Kafka.Configuration;
using Epiphany.Examples.Messaging;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace Epiphany.Examples.Kafka.Consumer
{
    public class KafkaConsumer : IConsumer
    {
        private readonly ILogger _logger;
        private readonly IMessageHandler _messageHandler;
        private readonly KafkaConfiguration _configuration;

        public KafkaConsumer(IConfiguration configuration, ILogger<KafkaConsumer> logger, IMessageHandler messageHandler)
        {
            _logger = logger;
            _messageHandler = messageHandler;

            _configuration = new KafkaConfiguration(configuration);
        }

        public Task<int> Listen(int timeout, CancellationToken cancellationToken)
        {
            _logger.LogInformation($"Started listening on topic {_configuration.TopicName}");
            var messageCounter = 0;

            var kafkaConsumerConfig = _configuration.ToKafkaConsumerConfig();
            using (var consumer = new Consumer<Ignore, string>(kafkaConsumerConfig))
            {
                consumer.Subscribe(_configuration.TopicName);

                var consuming = true;
                consumer.OnError += (_, e) => consuming = !e.IsFatal;

                var finishAt = DateTime.Now.AddSeconds(timeout);


                while ((timeout == 0 || DateTime.Now < finishAt) && consuming && !cancellationToken.IsCancellationRequested)
                {
                    try
                    {
                        var message = consumer.Consume();
                        _messageHandler.Handle(message.Topic, message.Value);
                        _logger.LogInformation($"Consumed message '{message.Value}' at: '{message.TopicPartitionOffset}'.");
                        if (timeout > 0) //count messages only if there is timeout defined
                        {
                            messageCounter++;
                        }
                    }
                    catch (ConsumeException e)
                    {
                        _logger.LogError($"Error occured: {e.Error.Reason}");
                    }
                }

                // Ensure the consumer leaves the group cleanly and final offsets are committed.
                consumer.Close();
            }
            _logger.LogInformation($"Finished listening on topic {_configuration.TopicName}, received: {messageCounter} messages.");
            return Task.FromResult(messageCounter);
        }

        /// <summary>
        /// Get Items read from queue. 
        /// </summary>
        /// <returns></returns>
        public async Task<IEnumerable<string>> GetItems()
        {
            var result = _messageHandler.History.ToList();
            return await Task.FromResult(result);
        }
    }
}
