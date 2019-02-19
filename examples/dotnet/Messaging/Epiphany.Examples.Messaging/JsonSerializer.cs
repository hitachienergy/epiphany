using Newtonsoft.Json;

namespace Epiphany.Examples.Messaging
{
    public class JsonSerializer : ISerializer
    {
        private readonly JsonSerializerSettings _serializerSettings;

        public JsonSerializer()
        {
            _serializerSettings = new JsonSerializerSettings();
        }
        public string Serialize<T>(T model)
        {
            return JsonConvert.SerializeObject(model, _serializerSettings);
        }
    }
}
