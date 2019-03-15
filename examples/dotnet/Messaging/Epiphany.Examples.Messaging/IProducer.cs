using System.Collections.Generic;
using System.Threading.Tasks;

namespace Epiphany.Examples.Messaging
{
    public interface IProducer
    {
        /// <summary>
        /// Publish to configured queue string messages. 
        /// </summary>
        /// <param name="models">List of string values.</param>
        /// <returns></returns>
        Task<bool> Produce(IEnumerable<string> models);
    }
}
