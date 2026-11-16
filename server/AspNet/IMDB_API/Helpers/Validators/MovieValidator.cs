using IMDB_API.Models.Requests;

namespace IMDB_API.Helpers.Validators
{
    public class MovieValidator
    {   
        public static void ValidateRequest(MovieRequest request)
        {
            ValidationHelper.ValidateNull(request, "Movie Request");

            ValidationHelper.ValidateString(request.Name, "Movie Name");
            //ValidationHelper.ValidateString(request.CoverImage, "Cover Image");
            ValidationHelper.ValidateString(request.Plot, "Movie Plot");
            ValidationHelper.ValidatePositiveInt(request.YearOfRelease, "Year of Release");
            ValidationHelper.ValidatePositiveInt(request.ProducerId, "Producer Id");
        }
    }
}
