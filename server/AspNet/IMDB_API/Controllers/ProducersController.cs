using IMDB_API.Models.Db;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using IMDB_API.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_Controllers.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class ProducersController : ControllerBase
    {
        private readonly IProducerService _producerService;
        public ProducersController(IProducerService producerService)
        {
            _producerService = producerService;
        }

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var producers = await _producerService.Get();

            return Ok(new ApiResponse<IEnumerable<ProducerResponse>>
            {
                data = producers
            });
        }

        [HttpGet("{id:int}")]
        public async Task<IActionResult> Get([FromRoute]int id)
        {
            var producer = await _producerService.Get(id);

            return Ok(new ApiResponse<ProducerResponse>
            {
                data = producer
            });
        }

        [HttpPost]
        public async Task<IActionResult> Add([FromBody]ProducerRequest request)
        {
            var id = await _producerService.Add(request);
            return CreatedAtAction(
                nameof(Get),
                new { id });
        }

        [HttpPut("{id:int}")]
        public async Task<IActionResult> Update([FromRoute] int id, [FromBody]ProducerRequest request)
        {
            await _producerService.Update(id, request);
            return Ok();
        }

        [HttpDelete("{id:int}")]
        public async Task<IActionResult> Delete([FromRoute] int id)
        {
            await _producerService.Delete(id);
            return NoContent();
        }
    }
}
