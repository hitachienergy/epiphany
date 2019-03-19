using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace Epiphany.Examples.Messaging
{
    public interface IConsumer
    {
        /// <summary>
        /// Listen on configured queue for a certain amount of time (timeout). Returns number of read messages
        /// </summary>
        /// <param name="timeout">Time for listening</param>
        /// <param name="cancellationToken"></param>
        /// <returns></returns>
        Task<int> Listen(int timeout, CancellationToken cancellationToken);

        Task<IEnumerable<string>> GetItems();
    }
}
