using IMDB_API.Models.Filters;

namespace IMDB_API.Helpers.Validators
{
    public static class ValidateFilter
    {
        public static void ValidateReview(ReviewFilter filter)
        {
            if (filter.MovieId.HasValue)
            {
                ValidationHelper.ValidatePositiveInt(filter.MovieId.Value, "Movie Id");
            }

            if (filter.UserId.HasValue)
            {
                ValidationHelper.ValidatePositiveInt(filter.UserId.Value, "User Id");
            }
        }

        public static void ValidateMovie(MovieFilter filter)
        {
            if (filter.Year.HasValue)
            {
                ValidationHelper.ValidatePositiveInt(filter.Year.Value, "Year");
            }
        }
    }
}
