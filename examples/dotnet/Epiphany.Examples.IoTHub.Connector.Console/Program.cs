using System;
using System.Threading;
using Epiphany.Examples.Kafka.Consumer;
using Epiphany.Examples.Kafka.Producer;
using Epiphany.Examples.Messaging;
using Epiphany.Examples.Messaging.ModelGeneration;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace Epiphany.Examples.IoTHub.Connector.Console
{
    class Program
    {
        static void Main(string[] args)
        {
            var serviceProvider = ConfigureServices();
            var logger = serviceProvider.GetService<ILogger<Program>>();
            logger.LogInformation("Listening IoT and producing to Kafka");
            StartProducer(serviceProvider);
        }

        private static void StartProducer(ServiceProvider serviceProvider)
        {
            var configuration = serviceProvider.GetService<IConfiguration>();
            var producer = serviceProvider.GetService<IProducer>();
            var iotHubConsumer = new IoTHubConsumer(producer, configuration);
            iotHubConsumer.Consume(CancellationToken.None).GetAwaiter().GetResult();                                               
        }

        private static ServiceProvider ConfigureServices()
        {
            var configuration = new ConfigurationBuilder()
                .AddEnvironmentVariables()
                .Build();
            var services = new ServiceCollection()
                .AddSingleton<IConfiguration>(configuration)
                .AddSingleton<ILoggerFactory, LoggerFactory>()
                .AddTransient<ISerializer, JsonSerializer>();   
  
            services.AddTransient<IProducer, KafkaProducer>();


            var minLogLevel = GetMinimalLogLevel(configuration);
            services.AddLogging(configure => configure.AddConsole())
                .Configure<LoggerFilterOptions>(options => options.MinLevel = minLogLevel);

            return services.BuildServiceProvider();
        }

        private static LogLevel GetMinimalLogLevel(IConfiguration configuration)
        {
            return configuration["ASPNETCORE_ENVIRONMENT"] == "Production" ? LogLevel.Warning : LogLevel.Debug;
        }
    }
}
