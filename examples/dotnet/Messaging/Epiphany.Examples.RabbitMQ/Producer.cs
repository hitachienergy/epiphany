using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Epiphany.Examples.Messaging;

namespace Epiphany.Examples.RabbitMQ
{
    public class Producer : IProducer
    {
        public Task<bool> Produce(IEnumerable<string> models)
        {
            throw new NotImplementedException();
        }
    }
}
