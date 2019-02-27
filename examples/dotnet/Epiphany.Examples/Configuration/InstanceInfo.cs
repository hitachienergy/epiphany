using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.Api.Configuration
{
    public interface IInstanceInfo
    {
        string NodeName { get; set; }
        string PodName { get; set; }
        string PodIp { get; set; }
        string Namespace { get; set; }
        string PodServiceAccount { get; set; }
        string QueueUsed { get; set; }
    }

    public class InstanceInfo : IInstanceInfo
    {
        public InstanceInfo(IConfiguration configuration)
        {
            NodeName = configuration["NODE_NAME"];
            PodName = configuration["POD_NAME"];
            PodIp = configuration["POD_IP"];
            Namespace = configuration["POD_NAMESPACE"];
            PodServiceAccount = configuration["POD_SERVICE_ACCOUNT"];
            QueueUsed = configuration["USE_QUEUE"];
        }

        public string NodeName { get; set; }
        public string PodName { get; set; }
        public string PodIp { get; set; }
        public string Namespace { get; set; }
        public string PodServiceAccount { get; set; }
        public string QueueUsed { get; set; }
    }
}
