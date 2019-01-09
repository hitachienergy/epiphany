using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace KeyCloak.Controllers
{
    public class AppController : Controller
    {
        public class LoginState
        { 
            public bool authenticated { get; set; }
        }

        public class ApiToken
        {
            public string token { get; set; }
        }

        private string GetBaseUrl()
        {
            var request = HttpContext.Request;
            var baseUrl = string.Format("{0}://{1}", request.Scheme, request.Host);
            return baseUrl;
        }

        [HttpGet]
        [Route("state")]
        public LoginState State()
        {
            return new LoginState()
            {
                authenticated = User.Identity.IsAuthenticated
            };
        }

        [HttpGet]
        [Route("token")]
        [Authorize()]
        public ApiToken Token()
        {
            return new ApiToken()
            {
                token = HttpContext.GetTokenAsync("access_token").Result
            };
        }

        [HttpGet]
        [Route("login")]
        [Authorize]
        public IActionResult Login()
        {
            return Redirect(GetBaseUrl());
        }

        [HttpGet]
        [Route("logout")]
        [Authorize]
        public async Task<RedirectResult> LogoutAsync()
        {
            /* 
            Logout has an issue where it doesnt support SSO logout at this point:
            https://github.com/aspnet/Security/issues/1712
            */
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            await HttpContext.SignOutAsync(OpenIdConnectDefaults.AuthenticationScheme);
            foreach (var cookie in Request.Cookies.Keys)
            {
                Response.Cookies.Delete(cookie);
            }
            return Redirect(GetBaseUrl());
        }
    }
}
