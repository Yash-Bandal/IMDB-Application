using IMDB_API.Models.Db;
using IMDB_API.Models.Filters;
using IMDB_API.Repository.Interfaces;
using Microsoft.Extensions.Options;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Repository
{
    public class ReviewRepository : BaseRepository<Review>, IReviewRepository
    {
        public ReviewRepository(IOptions<ConnectionString> connectionString)
            : base(connectionString.Value.IMDBConnection)
        {
        }

        public async Task<IEnumerable<Review>> Get(ReviewFilter filter)
        {
            const string query = @"
                SELECT
                    Id,
                    Message,
                    MovieId,
                    UserId
                FROM Foundation.Reviews
                WHERE
                    (@MovieId IS NULL OR MovieId = @MovieId)
                    AND
                    (@UserId IS NULL OR UserId = @UserId)";

            return await QueryAsync(
                query,
                new
                {
                    filter.MovieId,
                    filter.UserId
                });
        }

        public async Task<Review> Get(int movieId, int id)
        {
            const string query = @"
                SELECT
                    Id,
                    Message,
                    MovieId
                FROM Foundation.Reviews
                WHERE Id = @Id
                    AND MovieId = @MovieId";

            return await QuerySingleAsync(
                query,
                new
                {
                    Id = id,
                    MovieId = movieId
                }
            );
        }

        public async Task<int> Add(int movieId, Review review)
        {
            const string query = @"
                INSERT INTO Foundation.Reviews
                (
                    Message,
                    MovieId,
                    UserId
                )
                VALUES
                (
                    @Message,
                    @MovieId,
                    @UserId
                );

                SELECT CAST(SCOPE_IDENTITY() AS INT);";

            return await ExecuteScalarAsync<int>(
                query,
                new
                {
                    review.Message,
                    MovieId = movieId,
                    review.UserId
                }
            );
        }

        public async Task Update(int movieId, int id, Review review)
        {
            const string query = @"
                UPDATE Foundation.Reviews
                SET
                    Message = @Message
                WHERE Id = @Id
                    AND MovieId = @MovieId";

            await ExecuteAsync(
                query,
                new
                {
                    Id = id,
                    MovieId = movieId,
                    review.Message
                }
            );
        }

        public async Task Delete(int movieId, int id)
        {
            const string query = @"
                DELETE FROM Foundation.Reviews
                WHERE Id = @Id
                    AND MovieId = @MovieId";

            await ExecuteAsync(
                query,
                new
                {
                    Id = id,
                    MovieId = movieId
                }
            );
        }

        public async Task<bool> Exists(int id)
        {
            const string query = @"
                SELECT COUNT(1)
                FROM Foundation.Reviews
                WHERE Id = @Id";

            var count = await ExecuteScalarAsync<int>(
                query,
                new { Id = id });

            return count > 0;
        }

    }
}