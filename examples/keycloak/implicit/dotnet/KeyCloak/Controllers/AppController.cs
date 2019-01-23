using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;

namespace KeyCloak.Controllers
{
    public class AppController : Controller
    {
        public IConfiguration Configuration { get; }

        public class KeyCloakConfig
        { 
            public string realm { get; set; }
            public string clientId { get; set; }
            public string url { get; set; }
        }

        public AppController(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        [HttpGet]
        [Route("config")]
        public KeyCloakConfig Config()
        {
            return new KeyCloakConfig()
            {
                realm = Configuration["realm"],
                clientId = Configuration["clientid"],
                url = Configuration["url"]
            };
        }
    }
}
