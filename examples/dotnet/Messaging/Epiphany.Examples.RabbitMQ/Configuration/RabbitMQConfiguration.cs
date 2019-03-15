using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.RabbitMQ.Configuration
{
    public class RabbitMqConfiguration
    {
        public RabbitMqConfiguration(IConfiguration configuration)
        {
            TopicName = configuration["TOPIC_NAME"];
            Hostname = configuration["RABBITMQ_HOSTNAME"];
            Port = int.Parse(configuration["RABBITMQ_PORT"]);
            User = configuration["RABBITMQ_USER"];
            Password = configuration["RABBITMQ_PASSWORD"];
            Durable = configuration["RABBITMQ_DURABLE"] == "1";

        }

        public string Password { get; set; }

        public string User { get; set; }

        public int Port { get; set; }

        public bool Durable { get; set; }

        public string Hostname { get; set; }

        public string TopicName { get; set; }
    }
}
