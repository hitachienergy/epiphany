using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace Epiphany.Examples.Messaging
{
    public interface IProducer
    {
        Task<bool> Produce(IEnumerable<string> models);
    }
    public interface IConsumer
    {
        Task Consume(CancellationToken cancellationToken);
    }
}
