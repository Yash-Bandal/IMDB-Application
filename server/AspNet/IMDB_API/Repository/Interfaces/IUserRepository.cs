using IMDB_API.Models.Db;
using System.Threading.Tasks;

namespace IMDB_API.Repository.Interfaces
{
    public interface IUserRepository
    {
        Task Create(User user);
        Task<User> Get(string email);
    }
}