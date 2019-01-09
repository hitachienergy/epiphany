using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Clients.ActiveDirectory;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Epiphany.SampleApps.AuthService.Extensions
{
    public class CachedGraphClientTokenProvider
    {
        private readonly IConfiguration _configuration;
        public CachedGraphClientTokenProvider(IConfiguration configuration)
        {
            _configuration = configuration;
        }
        internal async Task<AuthenticationResult> GetToken(AzureAdConfig config)
        {
            ClientCredential clientCredential = new ClientCredential(config.ClientId, config.ClientSecret);
            AuthenticationContext ctx = new AuthenticationContext(_configuration["AzureAd:Instance"] + config.TenantId);

            AuthenticationResult result = null;
            try
            {
                result = await ctx.AcquireTokenAsync(config.Resource, clientCredential);
            }
            catch (AdalSilentTokenAcquisitionException exc)
            {
                throw exc;
            }
            catch (AdalException exc)
            {
                throw exc;
            }
            return result;

        }
    }
}
