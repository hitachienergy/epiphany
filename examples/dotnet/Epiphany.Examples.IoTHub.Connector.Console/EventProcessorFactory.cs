using Microsoft.Azure.EventHubs.Processor;
using System;
using System.Collections.Generic;
using System.Text;
using Epiphany.Examples.Messaging;
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.IoTHub.Connector.Console
{
    public class EventProcessorFactory : IEventProcessorFactory
    {
        private readonly IProducer producer;
        private readonly IConfiguration configuration;

        public EventProcessorFactory(IProducer producer, IConfiguration configuration)
        {
            this.producer = producer;
            this.configuration = configuration;
        }
        public IEventProcessor CreateEventProcessor(PartitionContext context)
        {
            return new SimpleEventProcessor(producer, configuration);
        }
    }
}
