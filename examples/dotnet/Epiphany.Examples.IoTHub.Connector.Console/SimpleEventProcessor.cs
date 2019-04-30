using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using Epiphany.Examples.Messaging;
using Microsoft.Azure.EventHubs;
using Microsoft.Azure.EventHubs.Processor;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json.Linq;

namespace Epiphany.Examples.IoTHub.Connector.Console
{
    public class SimpleEventProcessor : IEventProcessor
    {
        private readonly IProducer producer;
        private readonly string dataTopic;
        private readonly string configTopic;
        private readonly string eventTopic;
        private readonly string alarmTopic;

        public SimpleEventProcessor(IProducer producer, IConfiguration configuration)
        {
            this.producer = producer;
            dataTopic = configuration["DATA_TOPIC_NAME"];
            configTopic = configuration["CONFIG_TOPIC_NAME"];
            eventTopic = configuration["EVENT_TOPIC_NAME"];
            alarmTopic = configuration["ALARM_TOPIC_NAME"];
        }
        public Task CloseAsync(PartitionContext context, CloseReason reason)
        {
            System.Console.WriteLine($"Processor Shutting Down. Partition '{context.PartitionId}', Reason: '{reason}'.");
            return Task.CompletedTask;
        }

        public Task OpenAsync(PartitionContext context)
        {
            System.Console.WriteLine($"SimpleEventProcessor initialized. Partition: '{context.PartitionId}'");
            return Task.CompletedTask;
        }

        public Task ProcessErrorAsync(PartitionContext context, Exception error)
        {
            System.Console.WriteLine($"Error on Partition: {context.PartitionId}, Error: {error.Message}");
            return Task.CompletedTask;
        }

        public Task ProcessEventsAsync(PartitionContext context, IEnumerable<EventData> messages)
        {
            var routingDictionary = new Dictionary<string, List<string>>()
            {
                {dataTopic, new List<string>()},
                {eventTopic, new List<string>()},
                {configTopic, new List<string>()}
            };
            foreach (var eventData in messages)
            {
                var data = Encoding.UTF8.GetString(eventData.Body.Array, eventData.Body.Offset, eventData.Body.Count);
                var token = JToken.Parse(data);
                if (token is JArray)
                {
                    var batch = token.ToObject<List<JObject>>();
                    foreach (var item in batch)
                    {
                        var topic = GetTopicNameForMessage(item);
                        routingDictionary[topic].Add(data);
                    }
                }
                else if (token is JObject)
                {
                    JObject jsonMsg = JObject.Parse(data);
                    var topic = GetTopicNameForMessage(jsonMsg);
                    routingDictionary[topic].Add(data);
                }
            }

            foreach (var queue in routingDictionary)
            {
                if (queue.Value.Count > 0)
                {
                    //File.WriteAllText(@"D:\Backups\dump.txt", string.Join(",", queue.Value));
                    producer.Produce(queue.Value, queue.Key);
                }
            }
            return context.CheckpointAsync();
        }

        private string GetTopicNameForMessage(JObject jsonObject)
        {
            if (jsonObject.ContainsKey("event"))
            {
                return eventTopic;
            }
            if (jsonObject.ContainsKey("alarm"))
            {
                return alarmTopic;
            }
            if (jsonObject.ContainsKey("model"))
            {
                return dataTopic;
            }
            if (jsonObject.ContainsKey("message"))
            {
                return configTopic;
            }

            return "other-data";
        }
    }
}
