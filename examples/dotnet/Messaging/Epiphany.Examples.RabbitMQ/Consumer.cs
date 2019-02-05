using System;
using System.Threading;
using System.Threading.Tasks;
using Epiphany.Examples.Messaging;

namespace Epiphany.Examples.RabbitMQ
{
    public class Consumer : IConsumer
    {
        public Task Consume(CancellationToken cancellationToken)
        {
            throw new NotImplementedException();
        }
    }
}
