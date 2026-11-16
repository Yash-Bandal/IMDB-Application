using AutoMapper;
using IMDB_API.Helpers;
using IMDB_API.Helpers.Validators;
using IMDB_API.Models.Filters;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using IMDB_API.Repository;
using IMDB_API.Repository.Interfaces;
using IMDB_API.Services.Interfaces;
using IMDBSample.Models.Db;
using Microsoft.AspNetCore.Http;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace IMDB_API.Services
{
    public class MovieService : IMovieService
    {
        private readonly IMovieRepository _movieRepository;
        private readonly IMapper _mapper;

        private readonly IActorService _actorService;
        private readonly IProducerService _producerService;
        private readonly IGenreService _genreService;

        private readonly IStorageService _supabaseStorageService;

        public MovieService(
            IMovieRepository movieRepository,
            IActorService actorService,
            IProducerService producerService,
            IGenreService genreService,
            IStorageService supabaseStorageService,
            IMapper mapper)
        {
            _movieRepository = movieRepository;
            _actorService = actorService;
            _producerService = producerService;
            _genreService = genreService;
            _supabaseStorageService = supabaseStorageService;
            _mapper = mapper;
        }

        public async Task<IEnumerable<MovieResponse>> Get(MovieFilter filter)
        {
            ValidateFilter.ValidateMovie(filter);

            var movies = await _movieRepository.Get(filter);
            var responses = new List<MovieResponse>();

            foreach (var movie in movies)
            {
                responses.Add(await MapMovieResponse(movie));
            }

            return responses;
        }

        public async Task<MovieResponse> Get(int id)
        {
            ValidationHelper.ValidatePositiveInt(id, "Movie Id");

            var movie = await _movieRepository.Get(id);
            ValidationHelper.ValidateNotFound(movie, "Movie");

            return await MapMovieResponse(movie);
        }

        public async Task<int> Add(MovieRequest request)
        {
            MovieValidator.ValidateRequest(request);

            var duplicateExists = await _movieRepository.ExistsByNameAndYear(
                request.Name,
                request.YearOfRelease);

            if (duplicateExists)
            {
                throw new ValidationException(
                    "A movie with this name and release year already exists.");
            }

            var producerExists = await _producerService.Exists(request.ProducerId);
            ValidationHelper.ValidateExists(producerExists, "Producer");

            var actorIds = request.ActorIds ?? new List<int>();
            var genreIds = request.GenreIds ?? new List<int>();

            await _actorService.ValidateIdsExist(actorIds);
            await _genreService.ValidateIdsExist(genreIds);

            var movie = _mapper.Map<Movie>(request);

            return await _movieRepository.Add(movie, actorIds, genreIds);
        }


        public async Task Update(int id, MovieRequest request)
        {
            ValidationHelper.ValidatePositiveInt(id, "Movie Id");
            MovieValidator.ValidateRequest(request);

            var exists = await _movieRepository.Exists(id);
            ValidationHelper.ValidateExists(exists, "Actor");

            await _producerService.Get(request.ProducerId);

            var actorIds = request.ActorIds ?? new List<int>();
            var genreIds = request.GenreIds ?? new List<int>();

            await _actorService.ValidateIdsExist(actorIds);
            await _genreService.ValidateIdsExist(genreIds);

            var movie = _mapper.Map<Movie>(request);

            await _movieRepository.Update(id, movie, actorIds, genreIds);
        }

        public async Task Delete(int id)
        {
            ValidationHelper.ValidatePositiveInt(id, "Movie Id");

            var exists = await _movieRepository.Exists(id);
            ValidationHelper.ValidateExists(exists, "Actor");

            await _movieRepository.Delete(id);
        }


        public async Task<string> UpdatePoster(int movieId, IFormFile file)
        {
            ValidationHelper.ValidatePositiveInt(movieId, "Movie Id");
            ValidationHelper.ValidateNotFound(await _movieRepository.Get(movieId), "Movie");

            if (file == null || file.Length == 0)
            {
                throw new ValidationException("Poster image is required.");
            }

            var imageUrl = await _supabaseStorageService.UploadMoviePoster(movieId, file);

            await _movieRepository.UpdateCoverImage(movieId, imageUrl);

            return imageUrl;
        }

        private async Task<MovieResponse> MapMovieResponse(Movie movie)
        {
            var response = _mapper.Map<MovieResponse>(movie);

            response.Producer = await _producerService.Get(movie.ProducerId);

            response.Actors = await _actorService.GetByMovieId(movie.Id);
            response.Genres = await _genreService.GetByMovieId(movie.Id);

            return response;
        }

        public async Task<string> UploadPoster(IFormFile file)
        {
            if (file == null || file.Length == 0)
            {
                throw new ValidationException("Poster image is required.");
            }

            if (!file.ContentType.StartsWith("image/"))
            {
                throw new ValidationException("Only image files are allowed.");
            }

            return await _supabaseStorageService.UploadMoviePoster(file);
        }
    }
}