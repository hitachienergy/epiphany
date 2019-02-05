using System.Collections.Generic;
using System.Threading.Tasks;
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

        public MessagesController(IProducer producer)
        {
            _producer = producer;
        }

        [HttpPost]
        [Consumes("application/json")]
        public async Task<IActionResult> PostAsync([FromBody] JObject requestBody)
        {
            var msg = requestBody.ToString(Formatting.None);
            await _producer.Produce(new List<string> {msg});
            return Ok();
        }

        
        [HttpGet]
        public ActionResult<IEnumerable<string>> Get()
        {
            //todo get from topic "name"
            return new string[] { "value1", "value2" };
        }
    }
}
