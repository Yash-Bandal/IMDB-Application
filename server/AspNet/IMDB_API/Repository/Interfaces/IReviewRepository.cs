using IMDB_API.Models.Db;
using IMDB_API.Models.Filters;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Repository.Interfaces
{
    public interface IReviewRepository
    {
        Task<IEnumerable<Review>> Get(ReviewFilter filter);
        Task<Review> Get(int movieId, int id);

        Task<int> Add(int movieId, Review review);
        Task Update(int movieId, int id, Review review);
        Task Delete(int movieId, int id);

        Task<bool> Exists(int id);
    }
}
