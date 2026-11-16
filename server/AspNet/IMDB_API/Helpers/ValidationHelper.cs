using IMDB_API.CustomExceptions;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace IMDB_API.Helpers
{
    public static class ValidationHelper
    {
        public static void ValidateString(string value, string fieldVal)
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ValidationException($"{fieldVal} is Empty.");
        }

        public static void ValidateDate(DateTime date, string fieldVal)
        {
            if (date == default)
                throw new ValidationException($"Invalid {fieldVal}.");
        }

        public static void ValidatePositiveInt(int value, string fieldVal)
        {
            if (value <= 0)
                throw new ValidationException($"{fieldVal} must be greater than zero.");
        }

        public static void ValidateNull(object value, string fieldVal)
        {
            if (value == null)
                throw new ValidationException($"{fieldVal} was not found.");
        }

        public static void ValidateNotFound(object value, string fieldVal)
        {
            if (value == null)
                throw new EntityNotFoundException($"{fieldVal} was not found.");
        }

        public static void ValidateExists(bool exists, string fieldVal)
        {
            if (!exists)
            {
                throw new EntityNotFoundException($"{fieldVal} was not found.");
            }
        }

        public static void ValidateList<T>(IEnumerable<T> list, string fieldVal)
        {
            if (list == null || !list.Any())
                throw new ValidationException($"{fieldVal} is empty.");
        }

        public static void ValidateEmail(string email)
        {
            ValidateString(email, "Email Id");

            try
            {
                var mailAddress = new System.Net.Mail.MailAddress(email);
            }
            catch (FormatException)
            {
                throw new ValidationException("Invalid Email Id.");
            }
        }


        public static void ValidatePassword(string password)
        {
            ValidateString(password, "Password");

            if (password.Length < 8)
                throw new ValidationException(
                    "Password must contain at least 8 characters.");

            if (!password.Any(char.IsDigit))
                throw new ValidationException(
                    "Password must contain at least one number.");

            if (!password.Any(ch => !char.IsLetterOrDigit(ch)))
                throw new ValidationException(
                    "Password must contain at least one special character.");
        }

        public static void ValidateInvalidIds(IEnumerable<int> invalidIds)
        {
            if (invalidIds.Any())
            {
                throw new EntityNotFoundException(
                    $"Invalid Ids : {string.Join(", ", invalidIds)}");
            }
        }
    }
}