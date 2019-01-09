using Confluent.Kafka;
using Confluent.Kafka.Serialization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Options;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Epiphany.Kafka.WebProducer.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class KafkaController : ControllerBase
    {
        private readonly Producer<Null, string> _producer;
        private readonly IConfiguration _configuration;
        
        public KafkaController(IConfiguration configuration)
        {
            _configuration = configuration;
            var conf = new Dictionary<string, object>
            {
                { "group.id", _configuration["KAFKA_GROUP_ID"] },
                { "bootstrap.servers", _configuration["KAFKA_BOOTSTRAP_SERVERS"]},
                { "auto.commit.interval.ms", _configuration["KAFKA_AUTO_COMMIT_INVETRVAL_MS"] },
                { "auto.offset.reset", _configuration["KAFKA_AUTO_OFFSET_RESET"]},
                {"session.timeout.ms", _configuration["KAFKA_SESSION_TIMEOUT_MS"]},
            };

            _producer = new Producer<Null, string>(conf, null, new StringSerializer(Encoding.UTF8));
            //{
            //    for (int i = 0; i < 100; i++)
            //    {
            //        var dr = producer.ProduceAsync("foo", null, RandomString(10)).Result;
            //        Console.WriteLine($"Delivered '{dr.Value}' to: {dr.TopicPartitionOffset}");
            //    }
            //}
        }

        [HttpPost]
        public async void Post([FromBody]KafkaMessageModel model)
        {
            await _producer.ProduceAsync(model.Topic, null, model.Message);
            //var dr = producer.ProduceAsync("foo", null, RandomString(10)).Result;
            //Console.WriteLine($"Delivered '{dr.Value}' to: {dr.TopicPartitionOffset}");
        }
    }
}
