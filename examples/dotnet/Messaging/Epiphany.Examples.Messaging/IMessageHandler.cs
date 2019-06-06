using System.Collections.Concurrent;

namespace Epiphany.Examples.Messaging
{
    public interface IMessageHandler
    {
        void Handle(string topic, string message, bool unique = false);
        ConcurrentBag<string> History { get; }
        ConcurrentDictionary<string, string> PerTopicHistory { get; }
    }
}
