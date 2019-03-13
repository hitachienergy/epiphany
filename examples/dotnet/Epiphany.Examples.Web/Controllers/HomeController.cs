using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Epiphany.Examples.Web.Models;
using Microsoft.Extensions.Configuration;

namespace Epiphany.Examples.Web.Controllers
{
    public class HomeController : Controller
    {
        public HomeController(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Privacy()
        {
            return View();
        }

        public IActionResult InstanceInfo()
        {
            ViewData["NodeName"] = Configuration["NODE_NAME"];
            ViewData["Name"] = Configuration["POD_NAME"];
            ViewData["Namespace"] = Configuration["POD_NAMESPACE"];
            ViewData["PodIp"] = Configuration["POD_IP"];
            ViewData["ServiceAccount"] = Configuration["POD_SERVICE_ACCOUNT"];

            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
