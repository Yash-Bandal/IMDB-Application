using IMDB_API.Models.Db;

namespace IMDB_API.Services.Interfaces
{
    public interface IJwtService
    {
        string GenerateToken(User user);
    }
}