using AutoMapper;
using IMDB_API.Helpers;
using IMDB_API.Helpers.Validators;
using IMDB_API.Models.Db;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using IMDB_API.Repository;
using IMDB_API.Repository.Interfaces;
using IMDB_API.Services.Interfaces;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_API.Services
{
    public class ProducerService : IProducerService
    {
        private readonly IProducerRepository _producerRepository;
        private readonly IMapper _mapper;

        public ProducerService(IProducerRepository producerRepository, IMapper mapper)
        {
            _producerRepository = producerRepository;
            _mapper = mapper;
        }

        public async Task<IEnumerable<ProducerResponse>> Get()
        {
            var producers = await _producerRepository.Get();
            return _mapper.Map<IEnumerable<ProducerResponse>>(producers);
        }

        public async Task<ProducerResponse> Get(int id)
        {
            ValidationHelper.ValidatePositiveInt(id, "Producer Id");
            var producer = await _producerRepository.Get(id);
            ValidationHelper.ValidateNotFound(producer, "Producer");

            return _mapper.Map<ProducerResponse>(producer);
        }

        public async Task<int> Add(ProducerRequest request)
        {
            ProducerValidator.ValidateRequest(request);

            var producer = _mapper.Map<Producer>(request);
            producer.Id =  await _producerRepository.Add(producer);

            return producer.Id;
        }

        public async Task Update(int id, ProducerRequest request)
        {
            ValidationHelper.ValidatePositiveInt(id, "Producer Id");
            ProducerValidator.ValidateRequest(request);

            var exists = await _producerRepository.Exists(id);
            ValidationHelper.ValidateExists(exists, "Actor");

            var producer = _mapper.Map<Producer>(request);
            await _producerRepository.Update(id, producer);
        }

        public async Task Delete(int id)
        {
            ValidationHelper.ValidatePositiveInt(id, "Producer Id");

            var exists = await _producerRepository.Exists(id);
            ValidationHelper.ValidateExists(exists, "Actor");

            await _producerRepository.Delete(id);
        }

        public async Task<bool> Exists(int id)
        {
            ValidationHelper.ValidatePositiveInt(id, "Producer Id");
            return await _producerRepository.Exists(id);
        }
    }
}
