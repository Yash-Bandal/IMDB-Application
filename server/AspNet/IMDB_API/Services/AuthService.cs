using System.ComponentModel.DataAnnotations;
using System.Threading.Tasks;

using IMDB_API.Helpers;
using IMDB_API.Models.Authentication.Requests;
using IMDB_API.Models.Authentication.Responses;
using IMDB_API.Models.Db;
using IMDB_API.Repository.Interfaces;
using IMDB_API.Services.Interfaces;
using IMDB_API.Validators;

namespace IMDB_API.Services
{
    public class AuthService : IAuthService
    {
        private readonly IUserService _userService;
        private readonly IJwtService _jwtService;

        public AuthService(IUserService userService, IJwtService jwtService)
        {
            _userService = userService;
            _jwtService = jwtService;
        }

        public async Task<AuthResponse> SignUp(SignupRequest request)
        {
            ValidationHelper.ValidateNull(request, "Signup Request");

            request.Name = request.Name?.Trim();
            request.EmailId = request.EmailId?.Trim();

            UserValidator.ValidateSignup(request);

            var existingUser = await _userService.Get(request.EmailId);

            if (existingUser != null)
            {
                throw new ValidationException("Email Id already exists.");
            }

            var user = new User
            {
                Name = request.Name,
                Email = request.EmailId,
                Password = request.Password
            };

            await _userService.Create(user);

            var token = _jwtService.GenerateToken(user);

            return new AuthResponse
            {
                AccessToken = token
            };
        }

        public async Task<AuthResponse> Login(LoginRequest request)
        {
            ValidationHelper.ValidateNull(request, "Login Request");
            request.EmailId = request.EmailId.Trim();
            UserValidator.ValidateLogin(request);

            var user = await _userService.Get(request.EmailId);

            if (user == null || user.Password != request.Password)
            {
                throw new ValidationException("Invalid credentials.");
            }

            var token = _jwtService.GenerateToken(user);

            return new AuthResponse
            {
                AccessToken = token
            };
        }
    }
}