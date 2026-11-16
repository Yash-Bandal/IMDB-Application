using IMDB_API.Models.Db;
using System.Threading.Tasks;

namespace IMDB_API.Services.Interfaces
{
    public interface IUserService
    {
        Task Create(User user);
        Task<User> Get(string email);
    }
}