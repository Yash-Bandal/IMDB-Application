using AutoMapper;
using IMDB_API.Models.Db;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using IMDBSample.Models.Db;

namespace IMDB_API.Helpers.Mappings
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<ActorRequest, Actor>();
            CreateMap<Actor, ActorResponse>();

            CreateMap<ProducerRequest, Producer>();
            CreateMap<Producer, ProducerResponse>();

            CreateMap<GenreRequest, Genre>();
            CreateMap<Genre, GenreResponse>();

            CreateMap<ReviewRequest, Review>();
            CreateMap<Review, ReviewResponse>();

            CreateMap<MovieRequest, Movie>();
            CreateMap<Movie, MovieResponse>();
        }
    }
}
