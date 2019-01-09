using System.Collections.Generic;
using System.Security.Claims;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace KeyCloak.Controllers
{
    [Route("api/[controller]")]
    public class ValuesController : Controller
    {
        public class Item
        {
            public int id { get; set; }
            public string value { get; set; }
        }

        private static List<Item> data = new List<Item>
        {
            new Item(){
                id = 1,
                value = "1"
            },
            new Item(){
                id = 2,
                value = "2"
            },
            new Item(){
                id = 3,
                value = "3"
            },
             new Item(){
                id = 4,
                value = "4"
            },
        };

        public ValuesController()
        {
        }

        [HttpGet]
        [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme, Policy = "Administrator")]
        public IEnumerable<Item> Get()
        {
           return data;
        }

        [HttpGet("{id}")]
        [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
        public Item Get(int id)
        {
            return new Item()
            {
                id = id,
                value = "" + id
            };
        }
    }
}
