namespace IMDB_API.Models.Db
{
    public class Review
    {
        public int Id { get; set; }
        public string Message { get; set; }
        public int MovieId { get; set; }
        public int UserId { get; set; }
    }
}
