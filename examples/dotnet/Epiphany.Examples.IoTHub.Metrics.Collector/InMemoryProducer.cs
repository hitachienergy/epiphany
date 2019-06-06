using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Epiphany.Examples.Messaging;
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.IoTHub.Metrics.Collector
{
    public class InMemoryProducer : IProducer
    {
        private readonly IConfiguration configuration;
        private readonly IMessageHandler messageHandler;
        static ReaderWriterLock locker = new ReaderWriterLock();
        public InMemoryProducer(IConfiguration configuration, IMessageHandler messageHandler)
        {
            this.configuration = configuration;
            this.messageHandler = messageHandler;
        }
        public Task<bool> Produce(IEnumerable<string> models, string topicName = null)
        {
            try
            {
                locker.AcquireWriterLock(5000);
                File.WriteAllText(Path.Combine(configuration["PATH_TO_STORE"], topicName, $"{topicName}.prom"),
                    models.First().ToString());                
            }
            finally
            {
                locker.ReleaseWriterLock();
            }                                                        
          
            return Task.FromResult(true);
        }
    }
}
