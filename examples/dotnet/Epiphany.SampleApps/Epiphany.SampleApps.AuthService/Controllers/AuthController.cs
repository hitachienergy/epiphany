using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Epiphany.SampleApps.AuthService.Extensions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Clients.ActiveDirectory;

namespace Epiphany.SampleApps.AuthService.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly CachedGraphClientTokenProvider _tokenProvider;
        public AuthController(CachedGraphClientTokenProvider tokenProvider)
        {
            _tokenProvider = tokenProvider;
        }
        // POST: api/Auth    
        [HttpPost]
        public async Task<IActionResult> AcquireToken(AzureAdConfig config)
        {

            var result = await _tokenProvider.GetToken(config);

            return Ok(result.AccessToken);
        }

    }
}
