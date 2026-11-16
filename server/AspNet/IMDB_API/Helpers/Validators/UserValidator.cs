using IMDB_API.Helpers;
using IMDB_API.Models.Authentication.Requests;

namespace IMDB_API.Validators
{
    public static class UserValidator
    {
        public static void ValidateSignup(SignupRequest request)
        {
            ValidationHelper.ValidateNull(request, "Signup Request");

            ValidationHelper.ValidateString(request.Name, "User Name");
            ValidationHelper.ValidateEmail(request.EmailId);
            ValidationHelper.ValidatePassword(request.Password);
        }

        public static void ValidateLogin(LoginRequest request)
        {
            ValidationHelper.ValidateNull(request, "Login Request");

            ValidationHelper.ValidateEmail(request.EmailId);
            ValidationHelper.ValidatePassword(request.Password);
        }
    }
}