using System;
using System.Threading;
using Epiphany.Examples.Kafka.Consumer;
using Epiphany.Examples.Kafka.Producer;
using Epiphany.Examples.Messaging.ModelGeneration;
using Epiphany.Examples.RabbitMQ;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace Epiphany.Examples.Messaging.Console
{
    class Program
    {
        static void Main(string[] args)
        {
            var serviceProvider = ConfigureServices();
            var logger = serviceProvider.GetService<ILogger<Program>>();
            if(string.Equals(serviceProvider.GetService<IConfiguration>()["MODE"], "PRODUCER", StringComparison.InvariantCultureIgnoreCase))
            {
                logger.LogInformation("Started console in PRODUCER mode.");
                StartProducer(serviceProvider);
            }
            else
            {
                logger.LogInformation("Started console in CONSUMER mode.");
                StartConsumer(serviceProvider);
            }
        }

        private static void StartProducer(ServiceProvider serviceProvider)
        {
            var messageGenerator = serviceProvider.GetService<IMessageGenerator>();
            var messages = messageGenerator.Generate("DummyModel");

            var producer = serviceProvider.GetService<IProducer>();
            producer.Produce(messages).GetAwaiter().GetResult();
        }

        private static void StartConsumer(ServiceProvider serviceProvider)
        {
            var consumer = serviceProvider.GetService<IConsumer>();
            consumer.Listen(0, CancellationToken.None);
        }

        private static ServiceProvider ConfigureServices()
        {
            var configuration = new ConfigurationBuilder()
                .AddEnvironmentVariables()
                .Build();
            var services = new ServiceCollection()
            .AddSingleton<IConfiguration>(configuration)
            .AddSingleton<ILoggerFactory, LoggerFactory>()
            .AddTransient<ISerializer, JsonSerializer>()
            .AddTransient<IMessageGenerator, MessageGenerator>()
            .AddSingleton<IMessageHandler, MessageHandler>();
            if (configuration["USE_QUEUE"].Equals("Kafka", StringComparison.InvariantCultureIgnoreCase))
            {                                                     
                services.AddTransient<IProducer, KafkaProducer>();
                services.AddTransient<IConsumer, KafkaConsumer>();
            }
            else
            {                                                       
                services.AddTransient<IProducer, RabbitMqProducer>();
                services.AddTransient<IConsumer, RabbitMqConsumer>();
            }

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
