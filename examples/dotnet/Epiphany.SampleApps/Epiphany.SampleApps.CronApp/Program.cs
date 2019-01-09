using System;
using System.Threading;

namespace Epiphany.SampleApps.CronApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("CRON JOB EXECUTED!");
            Thread.Sleep(10000);
            Console.WriteLine("CRON JOB FINISHED!");
        }
    }
}
