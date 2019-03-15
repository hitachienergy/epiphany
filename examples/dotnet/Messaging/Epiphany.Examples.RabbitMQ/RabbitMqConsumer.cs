using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Epiphany.Examples.Messaging;
using Epiphany.Examples.RabbitMQ.Configuration;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using RabbitMQ.Client.MessagePatterns;

namespace Epiphany.Examples.RabbitMQ
{
    public class RabbitMqConsumer : IConsumer
    {
        private readonly IMessageHandler _messageHandler;
        private readonly ILogger _logger;
        private readonly RabbitMqConfiguration _defaultConfig;

        public RabbitMqConsumer(IConfiguration configuration, IMessageHandler messageHandler, ILogger<RabbitMqConsumer> logger)
        {
            _messageHandler = messageHandler;
            _logger = logger;
            _defaultConfig = new RabbitMqConfiguration(configuration);
        }

        public async Task<int> Listen(int timeout, CancellationToken cancellationToken)
        {
            try
            {
                var factory = new ConnectionFactory
                {
                    HostName = _defaultConfig.Hostname,
                    UserName = _defaultConfig.User,
                    Password = _defaultConfig.Password,
                    Port = _defaultConfig.Port
                };
                using (var connection = factory.CreateConnection())
                using (var channel = connection.CreateModel())
                {
                    channel.QueueDeclare(queue: _defaultConfig.TopicName,
                        durable: _defaultConfig.Durable,
                        exclusive: false,
                        autoDelete: false,
                        arguments: null);

                    var messageCounter = 0;

                    var subscription = new Subscription(channel, _defaultConfig.TopicName, false);

                    var finishAt = DateTime.Now.AddSeconds(timeout);
                    while ((timeout == 0 || DateTime.Now < finishAt) && !cancellationToken.IsCancellationRequested)
                    {
                        subscription.Next(5000, out var basicDeliveryEventArgs);
                        if (basicDeliveryEventArgs != null)
                        {
                            string messageContent = Encoding.UTF8.GetString(basicDeliveryEventArgs.Body);
                            _messageHandler.Handle(_defaultConfig.TopicName, messageContent);
                            subscription.Ack(basicDeliveryEventArgs);
                            if (timeout > 0) //count messages only if there is timeout defined
                            {
                                messageCounter++;
                            }
                        }
                    }

                    await Task.Delay(timeout * 1000, cancellationToken);

                    return await Task.FromResult(messageCounter);
                }
            }
            catch (Exception e)
            {
                _logger.LogError(e.ToString());
                throw;
            }
        }

        public async Task<IEnumerable<string>> GetItems()
        {
            var result = _messageHandler.History.ToList();
            return await Task.FromResult(result);
        }
    }
}
