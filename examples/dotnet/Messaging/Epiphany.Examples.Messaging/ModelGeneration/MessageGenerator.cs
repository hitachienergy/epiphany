using System;
using System.Collections.Generic;
using System.Linq;
using Epiphany.Examples.Messaging.Models;
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.Messaging.ModelGeneration
{
    public class MessageGenerator : IMessageGenerator
    {
        private readonly ISerializer _serializer;
        private readonly int _modelsNumber;
        private readonly int _parametersNumber;
        private readonly bool _produceInfinitely;

        public MessageGenerator(IConfiguration configuration, ISerializer serializer)
        {
            _serializer = serializer;
            _parametersNumber = int.Parse(configuration["PARAM_NUMBER"]);
            _modelsNumber = int.Parse(configuration["MODELS_NUMBER"]);
            _produceInfinitely = configuration["PRODUCE_INFINITELY"] == "1";
        }

        public IEnumerable<string> Generate(string prefixName)
        {
            while (true)
            {
                yield return GetMessage(prefixName);
                if (!_produceInfinitely)
                {
                    break;
                }
            }
        }

        private string GetMessage(string prefixName)
        {
            var models = new List<FakeModel>();
            for (var i = 0; i < _modelsNumber; i++)
            {
                models.Add(new FakeModel($"{prefixName}{i}")
                {
                    DateTime = DateTime.UtcNow,
                    Parameters = Enumerable.Range(0, _parametersNumber).Select(x => new FakeParameter($"Param00{x}")).ToList()
                });
            }
            return _serializer.Serialize(models);
        }
    }
}
