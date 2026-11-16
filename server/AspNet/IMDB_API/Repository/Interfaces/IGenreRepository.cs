using IMDB_API.Models.Db;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Repository.Interfaces
{
    public interface IGenreRepository
    {        
        Task<IEnumerable<Genre>> Get();
        Task<Genre> Get(int id);
        Task<IEnumerable<Genre>> GetByMovieId(int movieId);
        Task<int> Add(Genre genre);
        Task Update(int id, Genre genre);
        Task Delete(int id);

        Task<IEnumerable<int>> GetInvalidIds(IEnumerable<int> Ids);
        Task<bool> Exists(int id);
    }
}
