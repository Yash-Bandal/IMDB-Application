using Dapper;
using IMDB_API.Models.Db;
using IMDB_API.Models.Filters;
using IMDB_API.Repository.Interfaces;
using IMDBSample.Models.Db;
using Microsoft.Extensions.Options;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace IMDB_API.Repository
{
    public class MovieRepository : BaseRepository<Movie>, IMovieRepository
    {
        public MovieRepository(IOptions<ConnectionString> connectionString)
            : base(connectionString.Value.IMDBConnection)
        {
        }

        public async Task<IEnumerable<Movie>> Get(MovieFilter filter)
        {
            const string query = @"
                SELECT
                    Id,
                    Name,
                    YearOfRelease,
                    Plot,
                    CoverImage,
                    ProducerId
                FROM Foundation.Movies
                WHERE (@Year IS NULL OR YearOfRelease = @Year)";

            return await QueryAsync(
                query,
                new
                {
                    Year = filter.Year
                });
        }

        public async Task<Movie> Get(int id)
        {
            const string query = @"
                SELECT
                    Id,
                    Name,
                    YearOfRelease,
                    Plot,
                    CoverImage,
                    ProducerId
                FROM Foundation.Movies
                WHERE Id = @Id";

            return await QuerySingleAsync(
                query,
                new { Id = id });
        }

        public async Task<int> Add(
            Movie movie,
            IEnumerable<int> actorIds,
            IEnumerable<int> genreIds)
        {
            const string procedure = "Foundation.usp_AddMovie";

            return await ExecuteStoredProcedureAsync<int>(
                procedure,
                new
                {
                    movie.Name,
                    movie.YearOfRelease,
                    movie.Plot,
                    movie.CoverImage,
                    movie.ProducerId,
                    ActorIds = string.Join(",", actorIds),
                    GenreIds = string.Join(",", genreIds)
                });
        }


        public async Task Update(int id, Movie movie, IEnumerable<int> actorIds, IEnumerable<int> genreIds)
        {
            const string procedure = "Foundation.usp_UpdateMovie";

            await ExecuteStoredProcedureNonQueryAsync(
                procedure,
                new
                {
                    Id = id,
                    movie.Name,
                    movie.YearOfRelease,
                    movie.Plot,
                    movie.CoverImage,
                    movie.ProducerId,
                    ActorIds = string.Join(",", actorIds),
                    GenreIds = string.Join(",", genreIds)
                });
        }

        public async Task Delete(int id)
        {
            const string query = @"
                DELETE FROM Foundation.Actor_Movies
                WHERE MovieId = @Id;

                DELETE FROM Foundation.Genre_Movies
                WHERE MovieId = @Id;

                DELETE FROM Foundation.Reviews
                WHERE MovieId = @Id;

                DELETE FROM Foundation.Movies
                WHERE Id = @Id;";

            await ExecuteAsync(
                query,
                new { Id = id });
        }

        public async Task UpdateCoverImage(int movieId, string imageUrl)
        {
            const string query = @"
                UPDATE Foundation.Movies
                SET CoverImage = @ImageUrl
                WHERE Id = @MovieId";

            await ExecuteAsync(
                query,
                new
                {
                    MovieId = movieId,
                    ImageUrl = imageUrl
                });
        }

        public async Task<bool> Exists(int id)
        {
            const string query = @"
                SELECT COUNT(1)
                FROM Foundation.Movies
                WHERE Id = @Id";

            var count = await ExecuteScalarAsync<int>(
                query,
                new { Id = id });

            return count > 0;
        }

        public async Task<bool> ExistsByNameAndYear(string name, int year, int? excludeMovieId = null)
        {
            const string query = @"
                SELECT CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM Foundation.Movies
                        WHERE LOWER(LTRIM(RTRIM(Name))) =
                              LOWER(LTRIM(RTRIM(@Name)))
                          AND YearOfRelease = @Year
                          AND (@ExcludeMovieId IS NULL OR Id <> @ExcludeMovieId)
                    )
                    THEN CAST(1 AS BIT)
                    ELSE CAST(0 AS BIT)
                END";

            return await ExecuteScalarAsync<bool>(
                query,
                new
                {
                    Name = name,
                    Year = year,
                    ExcludeMovieId = excludeMovieId
                });
        }
    }
}