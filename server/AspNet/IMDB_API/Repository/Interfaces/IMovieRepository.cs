using IMDB_API.Models.Db;
using IMDB_API.Models.Filters;
using IMDBSample.Models.Db;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Repository.Interfaces
{
    public interface IMovieRepository
    {
        Task<IEnumerable<Movie>> Get(MovieFilter filter);
        Task<Movie> Get(int id);

        Task<int> Add(Movie movie, IEnumerable<int> actorIds, IEnumerable<int> genreIds);
        Task Update(int id, Movie movie, IEnumerable<int> actorIds, IEnumerable<int> genreIds);
        Task Delete(int id);

        Task UpdateCoverImage(int movieId, string imageUrl);

        Task<bool> Exists(int id);
        Task<bool> ExistsByNameAndYear(string name, int year, int? excludeMovieId = null);
    }
}