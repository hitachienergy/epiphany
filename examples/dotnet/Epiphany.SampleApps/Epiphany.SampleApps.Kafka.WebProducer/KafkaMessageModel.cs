using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Epiphany.Kafka.WebProducer
{
    public class KafkaMessageModel
    {
        [Required]
        public string Topic { get; set; }
        [Required]
        public string Message { get; set; }
    }
}
