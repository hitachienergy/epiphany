using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Epiphany.Examples.Api.Configuration;

namespace Epiphany.Examples.Api.Models
{
    public class MessagesResultModel
    {
        public IInstanceInfo InstanceInfo { get; set; }
        public List<string> Items { get; set; }
        public string ResultMessage { get; set; }
    }
}
