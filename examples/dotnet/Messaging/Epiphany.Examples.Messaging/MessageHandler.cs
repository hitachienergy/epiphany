using System;
using System.Collections.Concurrent;
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.Messaging
{
    public class MessageHandler : IMessageHandler
    {
        private readonly int _waitTimeMilliseconds;
        private readonly int _allowedElements = 100;

        public ConcurrentBag<string> History { get; }
        public ConcurrentDictionary<string, string> PerTopicHistory { get; }
        public MessageHandler(IConfiguration configuration)
        {
            if (!int.TryParse(configuration["WAIT_TIME"], out _waitTimeMilliseconds))
            {
                _waitTimeMilliseconds = 10;
            }
            History = new ConcurrentBag<string>();
            PerTopicHistory = new ConcurrentDictionary<string, string>();
        }
        public void Handle(string topic, string message, bool unique)
        {
            if (unique)
            {
                HandleDictionary(topic, message);
                return;
            }
            while (History.Count >= _allowedElements)
            {
                History.TryTake(out string result);
            }

            History.Add($"{topic}:{message}");
            System.Threading.Thread.Sleep(_waitTimeMilliseconds);
        }

        private void HandleDictionary(string topic, string message)
        {
            if (PerTopicHistory.ContainsKey(topic))
            {
                PerTopicHistory[topic] = message;
            }
            else
            {
                PerTopicHistory.TryAdd(topic, message);
            }
        }
    }
}
