using System.Collections.Generic;

namespace Epiphany.Examples.Messaging.ModelGeneration
{
    public interface IMessageGenerator
    {
        IEnumerable<string> Generate(string prefixName);
    }
}