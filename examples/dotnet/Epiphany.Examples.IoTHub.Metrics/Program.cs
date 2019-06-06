using Microsoft.Azure.Devices.Client;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;

namespace Epiphany.Examples.IoTHub.Metrics
{
    class Program
    {
        private static readonly HttpClient client = new HttpClient();

        private static string s_deviceConnectionString = Environment.GetEnvironmentVariable("IOTHUB_DEVICE_CONN_STRING");
        private static string metrics_url = Environment.GetEnvironmentVariable("EXPORTER_URL");
        private static string wait_time = Environment.GetEnvironmentVariable("WAIT_TIME");
        private static string hostname = Environment.GetEnvironmentVariable("NODE_NAME");

        // Select one of the following transports used by DeviceClient to connect to IoT Hub.
        private static TransportType s_transportType = TransportType.Mqtt; // TransportType.Amqp;

        static Dictionary<string, string> metricsExporters = new Dictionary<string, string>()
        {
            {"minion1", "192.168.100.102"},
            {"minion2", "192.168.100.105"},
            {"minion3", "192.168.100.106"},
            {"minion4", "192.168.100.104"},
            {"piboss", "192.168.100.103"},
        };

        static int Main(string[] args)
        {

            if (string.IsNullOrEmpty(s_deviceConnectionString) && args.Length > 0)
            {
                s_deviceConnectionString = args[0];
            }
            if (string.IsNullOrEmpty(wait_time))
            {
                wait_time = "10000";
            }
            if (string.IsNullOrEmpty(hostname))
            {
                throw new ArgumentNullException("Hostname not provided");
            }
            if (string.IsNullOrEmpty(metrics_url) && args.Length > 0)
            {
                metrics_url = $"http://{metricsExporters[hostname]}:9100/metrics";
            }


            DeviceClient deviceClient = DeviceClient.CreateFromConnectionString(s_deviceConnectionString, s_transportType);

            if (deviceClient == null)
            {
                Console.WriteLine("Failed to create DeviceClient!");
                return 1;
            }

            var client = new MetricsClient(deviceClient);
            while (true)
            {
                try
                {
                    var result = SendMetrics(client).GetAwaiter().GetResult();
                }
                catch (Exception e)
                {
                    Console.WriteLine(e);
                }
                System.Threading.Thread.Sleep(int.Parse(wait_time));
            }
            return 0;
        }

        static async Task<int> SendMetrics(MetricsClient client)
        {
            var message = await GetMetrics();
            await client.SendMetrics(message, hostname);
            return 0;
        }

        static async Task<string> GetMetrics()
        {

            var stringTask = client.GetStringAsync(metrics_url);

            var msg = await stringTask;

            return msg;
        }
    }
}
