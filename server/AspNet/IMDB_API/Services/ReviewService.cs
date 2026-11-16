using AutoMapper;
using IMDB_API.Helpers;
using IMDB_API.Helpers.Validators;
using IMDB_API.Models.Db;
using IMDB_API.Models.Filters;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using IMDB_API.Repository;
using IMDB_API.Repository.Interfaces;
using IMDB_API.Services.Interfaces;
using Microsoft.AspNetCore.Http;
using System.Collections.Generic;
using System.Security.Claims;
using System.Threading.Tasks;

namespace IMDB_API.Services
{
    public class ReviewService : IReviewService
    {
        private readonly IReviewRepository _reviewRepository;
        private readonly IHttpContextAccessor _httpContextAccessor;
        private readonly IMapper _mapper;

        public ReviewService(
            IReviewRepository reviewRepository,
            IMapper mapper,
            IHttpContextAccessor httpContextAccessor)
        {
            _reviewRepository = reviewRepository;
            _mapper = mapper;
            _httpContextAccessor = httpContextAccessor;
        }

        public async Task<IEnumerable<ReviewResponse>> Get(ReviewFilter filter)
        {
            ValidateFilter.ValidateReview(filter);
            var reviews = await _reviewRepository.Get(filter);

            return _mapper.Map<IEnumerable<ReviewResponse>>(reviews);
        }

        public async Task<ReviewResponse> Get(int movieId, int id)
        {
            ValidationHelper.ValidatePositiveInt(movieId, "Movie Id");
            ValidationHelper.ValidatePositiveInt(id, "Review Id");

            var review = await _reviewRepository.Get(movieId, id);
            ValidationHelper.ValidateNotFound(review, "Review");

            return _mapper.Map<ReviewResponse>(review);
        }

        public async Task<int> Add(int movieId, ReviewRequest request)
        {
            ReviewValidator.ValidateRequest(movieId, request);
            var review = _mapper.Map<Review>(request);

            var userIdClaim = _httpContextAccessor.HttpContext
                .User
                .FindFirst(ClaimTypes.NameIdentifier);

            var userId = int.Parse(userIdClaim.Value);
            review.UserId = userId;

            review.Id = await _reviewRepository.Add(movieId, review);

            return review.Id;
        }

        public async Task Update(int movieId, int id, ReviewRequest request)
        {
            ValidationHelper.ValidatePositiveInt(id, "Review Id");
            ReviewValidator.ValidateRequest(movieId, request);

            var exists = await _reviewRepository.Exists(id);
            ValidationHelper.ValidateExists(exists, "Actor");

            var review = _mapper.Map<Review>(request);
            await _reviewRepository.Update(movieId, id, review);
        }

        public async Task Delete(int movieId, int id)
        {
            ValidationHelper.ValidatePositiveInt(movieId, "Movie Id");
            ValidationHelper.ValidatePositiveInt(id, "Review Id");

            var exists = await _reviewRepository.Exists(id);
            ValidationHelper.ValidateExists(exists, "Actor");

            await _reviewRepository.Delete(movieId, id);
        }
    }
}
