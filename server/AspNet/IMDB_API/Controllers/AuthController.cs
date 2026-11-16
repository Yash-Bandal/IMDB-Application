using IMDB_API.Models.Authentication.Requests;
using IMDB_API.Models.Authentication.Responses;
using IMDB_API.Models.Responses;
using IMDB_API.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace IMDB_API.Controllers
{
    [AllowAnonymous]
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly IAuthService _authService;

        public AuthController(IAuthService authService)
        {
            _authService = authService;
        }

        [HttpPost("signup")]
        public async Task<IActionResult> SignUp([FromBody] SignupRequest request)
        {
            var response = await _authService.SignUp(request);
            return Ok(new ApiResponse<AuthResponse>
            {
                data = response
            });
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginRequest request)
        {
            var response = await _authService.Login(request);

            return Ok(new ApiResponse<AuthResponse>
            {
                data = response
            });
        }
    }
}