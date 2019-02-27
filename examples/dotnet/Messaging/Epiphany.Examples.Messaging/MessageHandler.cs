using System.Collections.Concurrent;
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.Messaging
{
    public class MessageHandler : IMessageHandler
    {
        private readonly int _waitTimeMilliseconds;
        private readonly int _allowedElements = 100;

        public ConcurrentBag<string> History { get; } 
        public MessageHandler(IConfiguration configuration)
        {
            if (!int.TryParse(configuration["WAIT_TIME"], out _waitTimeMilliseconds))
            {
                _waitTimeMilliseconds = 10;
            }
            History = new ConcurrentBag<string>();
        }
        public void Handle(string topic, string message)
        {
            while (History.Count >= _allowedElements)
            {
                History.TryTake(out string result);
            }

            History.Add($"{topic}:{message}");
            System.Threading.Thread.Sleep(_waitTimeMilliseconds);
        }
    }
}
