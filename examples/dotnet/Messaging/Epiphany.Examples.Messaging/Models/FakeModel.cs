using System;
using System.Collections.Generic;

namespace Epiphany.Examples.Messaging.Models
{
    public class FakeModel
    {
        public FakeModel(string name)
        {
            Name = name;
        }
        public string Name { get; set; }
        public DateTime DateTime { get; set; }
        public IEnumerable<FakeParameter> Parameters { get; set; }
    }
}
