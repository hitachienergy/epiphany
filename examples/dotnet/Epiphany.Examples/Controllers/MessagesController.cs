using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Epiphany.Examples.Api.Configuration;
using Epiphany.Examples.Api.Models;
using Epiphany.Examples.Messaging;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Epiphany.Examples.Api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MessagesController : ControllerBase
    {
        private readonly IProducer _producer;
        private readonly IConsumer _consumer;
        private readonly IInstanceInfo _instanceInfo;

        public MessagesController(IProducer producer, IConsumer consumer, IInstanceInfo instanceInfo)
        {
            _producer = producer;
            _consumer = consumer;
            _instanceInfo = instanceInfo;
        }

        /// <summary>
        /// Using POST request publish any message to specified (RabbitMQ or Kafka) queue.  
        /// </summary>
        /// <param name="requestBody">Any JSON object</param>
        /// <returns></returns>
        [HttpPost]
        [Consumes("application/json")]
        public async Task<IActionResult> PostAsync([FromBody] JObject requestBody)
        {
            try
            {
                var msg = requestBody.ToString(Formatting.None);
                await _producer.Produce(new List<string> { msg });
                return Ok(new MessagesResultModel { InstanceInfo = _instanceInfo, ResultMessage = "Successfully published message" });
            }
            catch (Exception exception)
            {
                return StatusCode(500, new MessagesResultModel
                {
                    InstanceInfo = _instanceInfo,
                    ResultMessage = $"Failed to publish: exception occured: {exception.Message}"
                });

            }

        }

        /// <summary>
        /// Using GET request get messages from specified queue (RabbitMQ or Kafka), queue will be listened for 1s. 
        /// </summary>
        /// <param name="token"></param>
        /// <returns></returns>
        [HttpGet]
        public async Task<ActionResult<IEnumerable<string>>> Get(CancellationToken token)
        {
            var count = await _consumer.Listen(1, token);
            var items = (await _consumer.GetItems()).ToList();
            return Ok(new MessagesResultModel { InstanceInfo = _instanceInfo, Items = items, ResultMessage = $"Messages received during listening: {count}, messages in memory: {items.Count}"});
        }
    }
}
