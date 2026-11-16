using IMDB_API.Models.Db;
using IMDB_API.Repository.Interfaces;
using Microsoft.Extensions.Options;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace IMDB_API.Repository
{
    public class ActorRepository : BaseRepository<Actor>, IActorRepository
    {
        public ActorRepository(IOptions<ConnectionString> connectionString)
            : base(connectionString.Value.IMDBConnection)
        {
        }

        public async Task<IEnumerable<Actor>> Get()
        {
            const string query = @"
                SELECT
                    Id,
                    Name,
                    Bio,
                    DateOfBirth AS DOB,
                    Gender
                FROM Foundation.Actors";

            return await QueryAsync(query);
        }

        public async Task<Actor> Get(int id)
        {
            const string query = @"
                SELECT
                    Id,
                    Name,
                    Bio,
                    DateOfBirth AS DOB,
                    Gender
                FROM Foundation.Actors
                WHERE Id = @Id";

            return await QuerySingleAsync(query, new { Id = id });
        }

        public async Task<IEnumerable<Actor>> GetByMovieId(int movieId)
        {
            const string query = @"
                SELECT
                    a.Id,
                    a.Name,
                    a.DateOfBirth,
                    a.Bio,
                    a.Gender
                FROM Foundation.Actors a
                INNER JOIN Foundation.Actor_Movies am
                    ON a.Id = am.ActorId
                WHERE am.MovieId = @MovieId";

            return await QueryAsync<Actor>(
                query,
                new { MovieId = movieId });
        }

        public async Task<int> Add(Actor actor)
        {
            const string query = @"
                INSERT INTO Foundation.Actors
                (
                    Name,
                    Bio,
                    DateOfBirth,
                    Gender
                )
                VALUES
                (
                    @Name,
                    @Bio,
                    @DOB,
                    @Gender
                )
                
                SELECT CAST(SCOPE_IDENTITY() AS INT)";


            return await ExecuteScalarAsync<int>(query, actor);
        }

        public async Task Update(int id, Actor actor)
        {
            const string query = @"
                UPDATE Foundation.Actors
                SET
                    Name = @Name,
                    Bio = @Bio,
                    DateOfBirth = @DOB,
                    Gender = @Gender
                WHERE Id = @Id";

            await ExecuteAsync(
                query,
                new
                {
                    Id = id,
                    actor.Name,
                    actor.Bio,
                    actor.DOB,
                    actor.Gender
                }
            );
        }

        public async Task Delete(int id)
        {
            const string query = @"
                DELETE FROM Foundation.Actors
                WHERE Id = @Id";
 
            await ExecuteAsync(query,  new { Id = id });
        }

        public async Task<IEnumerable<int>> GetInvalidIds(IEnumerable<int> ids)
        {
            const string query = @"
                SELECT Id
                FROM Foundation.Actors
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
                FROM Foundation.Actors
                WHERE Id = @Id";

            var count = await ExecuteScalarAsync<int>(
                query,
                new { Id = id });

            return count > 0;
        }

    }
}