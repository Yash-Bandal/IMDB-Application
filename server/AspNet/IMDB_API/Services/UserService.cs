using IMDB_API.Helpers;
using IMDB_API.Helpers.Validators;
using IMDB_API.Models.Db;
using IMDB_API.Repository.Interfaces;
using IMDB_API.Services.Interfaces;
using System.Threading.Tasks;

namespace IMDB_API.Services
{
    public class UserService : IUserService
    {
        private readonly IUserRepository _userRepository;

        public UserService(IUserRepository userRepository)
        {
            _userRepository = userRepository;
        }

        public async Task Create(User user)
        {
            ValidationHelper.ValidateNull(user, "User");
            ValidationHelper.ValidateString(user.Name, "User Name");
            ValidationHelper.ValidateEmail(user.Email);
            ValidationHelper.ValidatePassword(user.Password);

            await _userRepository.Create(user);
        }

        public async Task<User> Get(string email)
        {
            ValidationHelper.ValidateEmail(email);

            return await _userRepository.Get(email);
        }
    }
}