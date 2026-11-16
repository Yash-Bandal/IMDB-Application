using System.ComponentModel.DataAnnotations;

namespace IMDB_API.Models.Authentication.Requests
{
    public class SignupRequest
    {
        [Required]
        public string Name { get; set; }

        //[Required]
        //[EmailAddress]
        public string EmailId { get; set; }

        [Required]
        public string Password { get; set; }

    }
}
