using IMDB_API.Models.Db;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using System.Collections.Generic;
using System.Threading.Tasks;


namespace IMDB_API.Services.Interfaces
{
    public interface IActorService
    {
        Task<IEnumerable<ActorResponse>> Get();
        Task<ActorResponse> Get(int id);
        Task<IEnumerable<ActorResponse>> GetByMovieId(int movieId);

        Task<int> Add(ActorRequest request);
        Task Update(int id, ActorRequest request);
        Task Delete(int id);

        Task ValidateIdsExist(IEnumerable<int> ids);
    }
}
