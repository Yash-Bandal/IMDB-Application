using IMDB_API.Models.Requests;

namespace IMDB_API.Helpers.Validators
{
    public class ProducerValidator
    {
        public static void ValidateRequest(ProducerRequest request)
        {
            ValidationHelper.ValidateNull(request, "Producer Request");

            PersonValidator.ValidatePerson(
                request.Name,
                request.DOB,
                request.Bio,
                request.Gender);
        }
    }
}
