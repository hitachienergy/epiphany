using System;
using System.Threading;
using Epiphany.Examples.Api.Configuration;
using Epiphany.Examples.Kafka.Consumer;
using Epiphany.Examples.Kafka.Producer;
using Epiphany.Examples.Messaging;
using Epiphany.Examples.Messaging.ModelGeneration;
using Epiphany.Examples.RabbitMQ;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace Epiphany.Examples.Api
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_2);
            services.AddSingleton<IConfiguration>(Configuration);
            services.AddSingleton<ILoggerFactory, LoggerFactory>();
            services.AddTransient<ISerializer, JsonSerializer>();
            services.AddTransient<IMessageGenerator, MessageGenerator>();
            services.AddSingleton<IMessageHandler, MessageHandler>();
            services.AddTransient<IInstanceInfo, InstanceInfo>();
            if (Configuration["USE_QUEUE"].Equals("Kafka", StringComparison.InvariantCultureIgnoreCase))
            {
                services.AddTransient<IProducer, KafkaProducer>();
                services.AddTransient<IConsumer, KafkaConsumer>();
            }
            else
            {
                services.AddTransient<IProducer, RabbitMqProducer>();
                services.AddTransient<IConsumer, RabbitMqConsumer>();
            }
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
                app.UseHsts();
            }

            app.UseHttpsRedirection();
            app.UseMvc(routes =>
            {
                routes.MapRoute("default", "{controller=Messages}/{action=Get}");
            });
        }
    }
}
