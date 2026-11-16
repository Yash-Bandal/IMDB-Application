using IMDB_API.Models.Db;
using IMDB_API.Models.Filters;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Services.Interfaces
{
    public interface IReviewService
    {
        Task<IEnumerable<ReviewResponse>> Get(ReviewFilter filter);
        Task<ReviewResponse> Get(int movieId, int id);

        Task<int> Add(int movieId, ReviewRequest request);
        Task Update(int movieId, int id, ReviewRequest request);
        Task Delete(int movieId, int id);
    }
}
