using IMDB_API.Models.Db;
using IMDB_API.Repository.Interfaces;
using Microsoft.Extensions.Options;
using System.Threading.Tasks;

namespace IMDB_API.Repository
{
    public class UserRepository : BaseRepository<User>, IUserRepository
    {
        public UserRepository(IOptions<ConnectionString> connectionString)
            : base(connectionString.Value.IMDBConnection)
        {
        }

        public async Task Create(User user)
        {
            const string query = @"
                INSERT INTO Foundation.Users
                (
                    Name,
                    Email,
                    Password
                )
                VALUES
                (
                    @Name,
                    @Email,
                    @Password
                )";

            await ExecuteAsync(
                query,
                new
                {
                    user.Name,
                    user.Email,
                    user.Password
                });
        }

        public async Task<User> Get(string email)
        {
            const string query = @"
                SELECT
                    Id,
                    Name,
                    Email,
                    Password
                FROM Foundation.Users
                WHERE Email = @Email";

            return await QuerySingleAsync(
                query,
                new { Email = email });
        }
    }
}