using System;

namespace Epiphany.Examples.Messaging.Models
{
    public class FakeParameter
    {
        public FakeParameter(string name)
        {
            var random = new Random();
            Key = name;
            Value = random.NextDouble() * 1000;
        }
        public string Key { get; set; }
        public double Value { get; set; }
    }
}
