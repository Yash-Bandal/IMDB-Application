using IMDB_API.Services.Interfaces;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Options;
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
namespace IMDB_API.Services
{
    public class SupabaseStorageService : IStorageService
    {
        private readonly SupabaseSettings _settings;
        private readonly HttpClient _httpClient;

        public SupabaseStorageService(IOptions<SupabaseSettings> settings, HttpClient httpClient)
        {
            _settings = settings.Value;
            _httpClient = httpClient;
        }

        public async Task<string> UploadMoviePoster(int movieId, IFormFile file)
        {
            var fileExtension = System.IO.Path.GetExtension(file.FileName);
            var fileName = $"{Guid.NewGuid()}{fileExtension}";
            var filePath = $"movies/{movieId}/{fileName}";

            var uploadUrl =
                $"{_settings.Url}/storage/v1/object/" +
                $"{_settings.BucketName}/{filePath}";

            using var stream = file.OpenReadStream();
            using var content = new StreamContent(stream);

            content.Headers.ContentType = new MediaTypeHeaderValue(file.ContentType);

            using var request = new HttpRequestMessage(HttpMethod.Post, uploadUrl);

            request.Headers.Add("apikey", _settings.SecretKey);
            request.Content = content;

            var response = await _httpClient.SendAsync(request);

            response.EnsureSuccessStatusCode();

            var publicUrl =
                $"{_settings.Url}/storage/v1/object/public/" +
                $"{_settings.BucketName}/{filePath}";

            return publicUrl;
        }

        public async Task<string> UploadMoviePoster(IFormFile file)
        {
            if (file == null || file.Length == 0)
            {
                throw new ValidationException("Poster image is required.");
            }

            var fileExtension = System.IO.Path.GetExtension(file.FileName);
            var fileName = $"{Guid.NewGuid()}{fileExtension}";
            var filePath = $"movies/{fileName}";

            var uploadUrl =
                $"{_settings.Url}/storage/v1/object/" +
                $"{_settings.BucketName}/{filePath}";

            using var stream = file.OpenReadStream();
            using var content = new StreamContent(stream);

            content.Headers.ContentType =
                new MediaTypeHeaderValue(file.ContentType);

            using var request = new HttpRequestMessage(HttpMethod.Post, uploadUrl);

            request.Headers.Add("apikey", _settings.SecretKey);
            request.Content = content;

            var response = await _httpClient.SendAsync(request);

            response.EnsureSuccessStatusCode();

            var publicUrl =
                $"{_settings.Url}/storage/v1/object/public/" +
                $"{_settings.BucketName}/{filePath}";

            return publicUrl;
        }
    }
}