using IMDB_API.CustomExceptions;
using IMDB_API.Exceptions;
using IMDB_API.Models.Db;
using IMDB_API.Models.Requests;
using System.Collections.Generic;
using System.Linq;

namespace IMDB_API.Helpers.Validators
{
    public class ActorValidator
    {

        public static void ValidateRequest(ActorRequest request)
        {
            ValidationHelper.ValidateNull(request, "Actor Request");

            PersonValidator.ValidatePerson(
                request.Name,
                request.DOB,
                request.Bio,
                request.Gender);
        }

    }
}
