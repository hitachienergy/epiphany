using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Epiphany.Examples.IoTHub.Metrics;
using Epiphany.Examples.Messaging;
using Microsoft.Azure.EventHubs;        
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Epiphany.Examples.IoTHub.Connector.Console
{
    public class MetricsReceiver : IMetricsReceiver
    {
        private readonly IProducer producer;
        private readonly EventHubsConnectionStringBuilder connectionString;
        private EventHubClient s_eventHubClient;
        public MetricsReceiver(IProducer producer, IConfiguration configuration)
        {
            this.producer = producer;
            connectionString = new EventHubsConnectionStringBuilder(new Uri(configuration["EVENT_HUB_COMPATIBLE_ENDPOINT"]),
                configuration["EVENT_HUB_COMPATIBLE_PATH"],
                configuration["IOT_HUB_SAS_KEY_NAME"],
                configuration["IOT_HUB_SAS_KEY"]);

        }

        public async Task Receive()
        {
            // Create an EventHubClient instance to connect to the
            // IoT Hub Event Hubs-compatible endpoint.
            s_eventHubClient = EventHubClient.CreateFromConnectionString(connectionString.ToString());

            // Create a PartitionReciever for each partition on the hub.
            var runtimeInfo = await s_eventHubClient.GetRuntimeInformationAsync();
            var d2cPartitions = runtimeInfo.PartitionIds;

            CancellationTokenSource cts = new CancellationTokenSource();

            var tasks = new List<Task>();
            foreach (string partition in d2cPartitions)
            {
                tasks.Add(ReceiveMessagesFromDeviceAsync(partition, cts.Token));
            }

            // Wait for all the PartitionReceivers to finsih.
            Task.WaitAll(tasks.ToArray());
        }

        private async Task ReceiveMessagesFromDeviceAsync(string partition, CancellationToken ct)
        {
            // Create the receiver using the default consumer group.
            // For the purposes of this sample, read only messages sent since 
            // the time the receiver is created. Typically, you don't want to skip any messages.
            var eventHubReceiver = s_eventHubClient.CreateReceiver("$Default", partition, EventPosition.FromEnqueuedTime(DateTime.Now));
            while (true)
            {
                if (ct.IsCancellationRequested) break;
                // Check for EventData - this methods times out if there is nothing to retrieve.
                var events = await eventHubReceiver.ReceiveAsync(100);

                // If there is data in the batch, process it.
                if (events == null) continue;

                foreach (EventData eventData in events)
                {
                    string data = Encoding.UTF8.GetString(eventData.Body.Array);
                    try
                    {
                        var model = JsonConvert.DeserializeObject<MetricsModel>(data);
                        await producer.Produce(new List<string>() { model.Data }, model.Name);
                    }
                    catch (Exception e)
                    {
                        System.Console.WriteLine(e);
                    }

                    //foreach (var prop in eventData.Properties)
                    //{
                    //    Console.WriteLine("  {0}: {1}", prop.Key, prop.Value);
                    //}
                    //Console.WriteLine("System properties (set by IoT Hub):");
                    //foreach (var prop in eventData.SystemProperties)
                    //{
                    //    Console.WriteLine("  {0}: {1}", prop.Key, prop.Value);
                    //}
                }
            }
        }
    }
}
