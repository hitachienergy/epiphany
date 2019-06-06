using System.Threading;
using Epiphany.Examples.IoTHub.Metrics.Collector;
using Epiphany.Examples.Messaging;
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
            logger.LogInformation("Listening IoT and producing to InMemoryStore");
            StartConsumer(serviceProvider);
        }

        private static void StartConsumer(ServiceProvider serviceProvider)
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
  
            services.AddTransient<IMessageHandler, MessageHandler>();
            services.AddTransient<IProducer, InMemoryProducer>();


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
