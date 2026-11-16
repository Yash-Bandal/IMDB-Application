using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;

namespace IMDB_API.Services.Interfaces
{
    public interface IStorageService
    {
        Task<string> UploadMoviePoster(int movieId, IFormFile file);
        Task<string> UploadMoviePoster(IFormFile file);
    }
}