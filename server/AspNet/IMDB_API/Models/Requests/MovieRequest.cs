using System.Collections.Generic;

namespace IMDB_API.Models.Requests
{
    public class MovieRequest
    {
        public string Name { get; set; }
        public int YearOfRelease { get; set; }
        public string Plot { get; set; }
        public string CoverImage { get; set; }
        public int ProducerId { get; set; }

        public IEnumerable<int> ActorIds { get; set; }
        public IEnumerable<int> GenreIds { get; set; }
    }
}
