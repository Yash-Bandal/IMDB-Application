using IMDB_API.Models.Db;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using IMDB_API.Repository;
using Microsoft.AspNetCore.Cors.Infrastructure;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Services.Interfaces
{
    public interface IProducerService
    {
        Task<IEnumerable<ProducerResponse>> Get();
        Task<ProducerResponse> Get(int id);

        Task<int> Add(ProducerRequest request);
        Task Update(int id, ProducerRequest request);
        Task Delete(int id);

        Task<bool> Exists(int id);

    }
}
