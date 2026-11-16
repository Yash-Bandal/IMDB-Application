using IMDB_API.Models.Filters;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using Microsoft.AspNetCore.Http;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Services.Interfaces
{
    public interface IMovieService
    {
        Task<IEnumerable<MovieResponse>> Get(MovieFilter filter);
        Task<MovieResponse> Get(int id);

        Task<int> Add(MovieRequest request);
        Task Update(int id, MovieRequest request);
        Task Delete(int id);

        Task<string> UpdatePoster(int movieId, IFormFile file);
        Task<string> UploadPoster(IFormFile file);
    }
}