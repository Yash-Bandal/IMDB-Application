using IMDB_API.Models.Db;
using System.Collections;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace IMDB_API.Repository.Interfaces
{
    public interface IProducerRepository
    {
        Task<IEnumerable<Producer>> Get();
        Task<Producer> Get(int id);

        Task<int> Add(Producer producer);
        Task Update(int id, Producer producer);
        Task Delete(int id);

        Task<bool> Exists(int id);
    }
}
