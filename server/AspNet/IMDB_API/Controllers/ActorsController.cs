using AutoMapper;
using IMDB_API;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using IMDB_API.Repository;
using IMDB_API.Services;
using IMDB_API.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_Controllers.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class ActorsController : ControllerBase
    {
        private readonly IActorService _actorService;

        public ActorsController(IActorService actorService)
        {
            _actorService = actorService;
        }

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var actors = await _actorService.Get();

            return Ok(new ApiResponse<IEnumerable<ActorResponse>>
            {
                data = actors
            });
        }

        [HttpGet("{id:int}")]
        public async Task<IActionResult> Get([FromRoute]int id)
        {
            var actor = await _actorService.Get(id);

            return Ok(new ApiResponse<ActorResponse>
            {
                data = actor
            });
        }

        [HttpPost]
        public async Task<IActionResult> Add([FromBody] ActorRequest request)
        {
            int id = await _actorService.Add(request);

            return CreatedAtAction(
                nameof(Get),
                new { id });
        }
        

        [HttpPut("{id:int}")]   
        public async Task<IActionResult> Update([FromRoute]int id, [FromBody]ActorRequest request)
        {
            await _actorService.Update(id, request);
            return Ok();
        }

        [HttpDelete("{id:int}")]
        public async Task<IActionResult> Delete([FromRoute] int id)
        {
            await _actorService.Delete(id);
            return NoContent();
        }
    }
}
