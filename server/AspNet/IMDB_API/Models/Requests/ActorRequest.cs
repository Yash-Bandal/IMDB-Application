using System;

namespace IMDB_API.Models.Requests
{
    public class ActorRequest
    {
        public string Name { get; set; }
        public string Bio { get; set; }
        public DateTime DOB { get; set; }
        public string Gender { get; set; }
    }
}
