using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Epiphany.SampleApps.AuthService.Extensions
{
    public class AzureAdConfig
    {
        public string TenantId { get; set; }
        public string ClientId { get; set; }
        public string Resource { get; set; }
        public string ClientSecret { get; set; }
    }
}
