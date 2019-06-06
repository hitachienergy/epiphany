using Microsoft.Azure.Devices.Client;
using Newtonsoft.Json;
using System;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace Epiphany.Examples.IoTHub.Metrics
{
    public class MetricsClient
    {
        private DeviceClient _deviceClient;

        public MetricsClient(DeviceClient deviceClient)
        {
            _deviceClient = deviceClient ?? throw new ArgumentNullException(nameof(deviceClient));
        }

        public async Task SendMetrics(string message, string topic)
        {
            var model = new MetricsModel
            {
                Name = topic,
                Data = message
            };
            var messageString = JsonConvert.SerializeObject(model);

            Message eventMessage = new Message(Encoding.UTF8.GetBytes(messageString));
            await _deviceClient.SendEventAsync(eventMessage).ConfigureAwait(false);
        }
    }
}
