using System.Threading;
using Epiphany.Examples.Messaging;
using System.Threading.Tasks;
using Microsoft.Azure.EventHubs;    
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.IoTHub.Connector.Console
{
    public class IoTHubConsumer
    {
        private readonly string EventHubConnectionString;
        private readonly string EventHubName;
        private readonly string StorageContainerName;
        private readonly string StorageAccountName;
        private readonly string StorageAccountKey;
        private readonly string StorageConnectionString; 
        private readonly IProducer producer;
        private readonly IConfiguration configuration;

        public IoTHubConsumer(IProducer producer, IConfiguration configuration)
        {
            this.producer = producer;
            this.configuration = configuration;
        }

        public async Task Consume(CancellationToken token)
        {
            var consumer = new MetricsReceiver(producer, configuration);
            await consumer.Receive();

            //await eventProcessorHost.RegisterEventProcessorAsync<SimpleEventProcessor>();
            while (!token.IsCancellationRequested)
            {

            }

            await Task.CompletedTask;
        }
    }
}
