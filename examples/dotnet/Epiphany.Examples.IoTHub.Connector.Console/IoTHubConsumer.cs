using System.Threading;
using Epiphany.Examples.Messaging;
using System.Threading.Tasks;
using Microsoft.Azure.EventHubs;
using Microsoft.Azure.EventHubs.Processor;    
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
            EventHubConnectionString = configuration["EVENTHUB_CONNECTIONSTRING"];
            EventHubName = configuration["EVENTHUB_NAME"];
            StorageContainerName = configuration["STORAGE_CONTAINER_NAME"];
            StorageAccountName = configuration["STORAGE_ACCOUNT_NAME"];
            StorageAccountKey = configuration["STORAGE_ACCOUNT_KEY"];

            StorageConnectionString = string.Format("DefaultEndpointsProtocol=https;AccountName={0};AccountKey={1}", StorageAccountName, StorageAccountKey);

        }

        public async Task Consume(CancellationToken token)
        {
            var eventProcessorHost = new EventProcessorHost(
                EventHubName,
                PartitionReceiver.DefaultConsumerGroupName,
                EventHubConnectionString,
                StorageConnectionString,
                StorageContainerName);

            // Registers the Event Processor Host and starts receiving messages
            await eventProcessorHost.RegisterEventProcessorFactoryAsync(new EventProcessorFactory(producer, configuration));
            //await eventProcessorHost.RegisterEventProcessorAsync<SimpleEventProcessor>();
            while (!token.IsCancellationRequested)
            {

            }

            await Task.CompletedTask;
        }
    }
}
