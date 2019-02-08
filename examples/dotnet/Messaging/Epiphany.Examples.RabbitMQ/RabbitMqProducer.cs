using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using Epiphany.Examples.Messaging;
using Epiphany.Examples.RabbitMQ.Configuration;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RabbitMQ.Client;

namespace Epiphany.Examples.RabbitMQ
{
    public class RabbitMqProducer : IProducer
    {
        private readonly ILogger _logger;
        private readonly RabbitMqConfiguration _defaultConfig;

        public RabbitMqProducer(IConfiguration configuration, ILogger<RabbitMqProducer> logger)
        {
            _logger = logger;
            _defaultConfig = new RabbitMqConfiguration(configuration);
        }


        public Task<bool> Produce(IEnumerable<string> models)
        {
            var factory = new ConnectionFactory
            {
                HostName = _defaultConfig.Hostname,
                UserName = _defaultConfig.User,
                Password = _defaultConfig.Password,
                Port = _defaultConfig.Port
            };
            try
            {
                using (var connection = factory.CreateConnection())
                {
                    using (var channel = connection.CreateModel())
                    {
                        channel.QueueDeclare(queue: _defaultConfig.TopicName,
                            durable: _defaultConfig.Durable,
                            exclusive: false,
                            autoDelete: false,
                            arguments: null);

                        foreach (var model in models)
                        {
                            var body = Encoding.UTF8.GetBytes(model);

                            channel.BasicPublish(exchange: "",
                                routingKey: _defaultConfig.TopicName,
                                basicProperties: null,
                                body: body);
                        }

                        return Task.FromResult(true);
                    }
                }
            }
            catch (Exception e)
            {
                _logger.LogError(e.ToString());
                throw;
            }
        }
    }
}
