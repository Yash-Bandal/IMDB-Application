using IMDB_API.Models.Authentication.Requests;
using IMDB_API.Models.Authentication.Responses;
using System.Threading.Tasks;

namespace IMDB_API.Services.Interfaces
{
    public interface IAuthService
    {
        Task<AuthResponse> SignUp(SignupRequest request);
        Task<AuthResponse> Login(LoginRequest request);
    }
}