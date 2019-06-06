using System.Threading.Tasks;

namespace Epiphany.Examples.IoTHub.Connector.Console
{
    public interface IMetricsReceiver
    {
        Task Receive();
    }
}
