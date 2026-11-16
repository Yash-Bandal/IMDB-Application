using System.ComponentModel.DataAnnotations;

namespace IMDB_API.Models.Authentication.Requests
{
    public class LoginRequest
    {
        [Required]
        [EmailAddress]
        public string EmailId { get; set; }

        [Required]
        public string Password { get; set; }
    }
}
