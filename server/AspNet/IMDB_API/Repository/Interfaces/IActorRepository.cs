using IMDB_API.Models.Db;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Repository.Interfaces
{
    public interface IActorRepository
    {
        Task<IEnumerable<Actor>> Get();
        Task<Actor> Get(int id);
        Task<IEnumerable<Actor>> GetByMovieId(int movieId);

        Task<int> Add(Actor actor);
        Task Update(int id, Actor actor);
        Task Delete(int id);

        Task<IEnumerable<int>> GetInvalidIds(IEnumerable<int> ids);
        Task<bool> Exists(int id);
    }
}
