using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.Messaging
{
    public interface IMessageHandler
    {
        void Handle(string topic, string message);
    }

    public class MessageHandler : IMessageHandler
    {
        private readonly int _waitTimeMilliseconds;

        public MessageHandler(IConfiguration configuration)
        {
            if (!int.TryParse(configuration["WAIT_TIME"], out _waitTimeMilliseconds))
            {
                _waitTimeMilliseconds = 10;
            }
        }
        public void Handle(string topic, string message)
        {
            System.Threading.Thread.Sleep(_waitTimeMilliseconds);
        }
    }
}
