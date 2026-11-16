using IMDB_API.Models.Db;
using IMDB_API.Models.Requests;
using System.Threading.Tasks;
using IMDB_API.Repository.Interfaces;
using Microsoft.Extensions.Options;
using System.Collections.Generic;
using System.Linq;

namespace IMDB_API.Repository
{
    public class ProducerRepository : BaseRepository<Producer>, IProducerRepository
    {
        public ProducerRepository(IOptions<ConnectionString> connectionString)
            : base (connectionString.Value.IMDBConnection)
        {
        }
        public async Task<IEnumerable<Producer>> Get()
        {
            const string query = @"
                SELECT
                    Id,
                    Name,
                    Bio,
                    DateOfBirth AS DOB,
                    Gender
                FROM Foundation.Producers";

            return await QueryAsync(query);
        }

        public async Task<Producer> Get(int id)
        {
            const string query = @"
                SELECT
                    Id,
                    Name,
                    Bio,
                    DateOfBirth AS DOB,
                    Gender
                FROM Foundation.Producers
                WHERE Id = @Id";

            return await QuerySingleAsync(query, new {Id = id});
        }

        public async Task<int> Add(Producer producer)
        {
            const string query = @"
                INSERT INTO Foundation.Producers
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

            return await ExecuteScalarAsync<int>(query, producer);
        }

        public async Task Update(int id, Producer producer)
        {
            const string query = @"
                UPDATE Foundation.Producers
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
                    producer.Name,
                    producer.Bio,
                    producer.DOB,
                    producer.Gender
                }
            );
        }

        public async Task Delete(int id)
        {
            const string query = @"
                DELETE FROM Foundation.Producers
                WHERE Id = @Id";

            await ExecuteAsync(query, new { Id = id });
        }

        public async Task<bool> Exists(int id)
        {
            const string query = @"
                SELECT COUNT(1)
                FROM Foundation.Producers
                WHERE Id = @Id";

            var count = await ExecuteScalarAsync<int>(
                query,
                new { Id = id });

            return count > 0;
        }
    }
}
