using System.Collections.Concurrent;

namespace Epiphany.Examples.Messaging
{
    public interface IMessageHandler
    {
        void Handle(string topic, string message);
        ConcurrentBag<string> History { get; }
    }
}
