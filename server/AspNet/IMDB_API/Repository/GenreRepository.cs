using IMDB_API.Models.Db;
using IMDB_API.Repository.Interfaces;
using Microsoft.Extensions.Options;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;

namespace IMDB_API.Repository
{
    public class GenreRepository : BaseRepository<Genre>, IGenreRepository
    {
        public GenreRepository(IOptions<ConnectionString> connectionString)
            : base (connectionString.Value.IMDBConnection)
        {
        }

        public async Task<IEnumerable<Genre>> Get()
        {
            const string query = @"
                SELECT
                    Id,
                    Name
                FROM Foundation.Genres";

            return await QueryAsync(query);
        }

        public async Task<Genre> Get(int id)
        {
            const string query = @"
                SELECT
                    Id,
                    Name
                FROM Foundation.Genres
                WHERE Id = @Id";

            return await QuerySingleAsync(query, new { Id = id });
        }

        public async Task<IEnumerable<Genre>> GetByMovieId(int movieId)
        {
            const string query = @"
                SELECT
                    g.Id,
                    g.Name
                FROM Foundation.Genres g
                INNER JOIN Foundation.Genre_Movies gm
                    ON g.Id = gm.GenreId
                WHERE gm.MovieId = @MovieId";

            return await QueryAsync<Genre>(
                query,
                new { MovieId = movieId });
        }

        public async Task<int> Add(Genre genre)
        {
            const string query = @"
                INSERT INTO Foundation.Genres
                (
                    Name
                )
                VALUES
                (
                    @Name
                )
                
                SELECT CAST(SCOPE_IDENTITY() AS INT)";


            return await ExecuteScalarAsync<int>(query, genre);
        }

        public async Task Update(int id, Genre genre)
        {
            const string query = @"
                UPDATE Foundation.Genres
                SET
                    Name = @Name
                WHERE Id = @Id";

            await ExecuteAsync(
                query,
                new
                {
                    Id = id,
                    genre.Name
                }
            );
        }

        public async Task Delete(int id)
        {
            const string query = @"
                DELETE FROM Foundation.Genres
                WHERE Id = @Id";

            await ExecuteAsync(query, new { Id = id });
        }

        public async Task<IEnumerable<int>> GetInvalidIds(IEnumerable<int> ids)
        {
            const string query = @"
                SELECT Id
                FROM Foundation.Genres
                WHERE Id IN @Ids";

            var validIds = await QueryAsync<int>(
                query,
                new { Ids = ids });

            return ids.Except(validIds);
        }

        public async Task<bool> Exists(int id)
        {
            const string query = @"
                SELECT COUNT(1)
                FROM Foundation.Genres
                WHERE Id = @Id";

            var count = await ExecuteScalarAsync<int>(
                query,
                new { Id = id });

            return count > 0;
        }
    }
}
