using IMDB_API.Exceptions;
using IMDB_API.Helpers;
using Microsoft.VisualBasic;
using System;
using System.Linq;

namespace IMDB_API.Helpers.Validators
{
    public class PersonValidator
    {
        public static void ValidatePerson(string name, DateTime dob, string bio, string gender)
        {
            ValidationHelper.ValidateString(name, "name");
            ValidationHelper.ValidateString(gender, "Gender");
            ValidationHelper.ValidateDate(dob, "Birthdate");
            ValidationHelper.ValidateString(bio, "Biography");

            if (!name.Any(char.IsLetter))
                throw new ValidationException("Name must contain Letters.");

            if (dob > DateTime.Today)
                throw new ValidationException("Date of Birth cannot be in Future.");
        }
    }
}
