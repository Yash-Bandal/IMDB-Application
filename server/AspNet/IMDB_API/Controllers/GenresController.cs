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
    public class GenresController : ControllerBase
    {
        private readonly IGenreService _genreService;
        public GenresController(IGenreService genreService)
        {
            _genreService = genreService;
        }

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var genres = await _genreService.Get();
            return Ok(new ApiResponse<IEnumerable<GenreResponse>>
            {
                data = genres
            });
        }

        [HttpGet("{id:int}")]
        public async Task<IActionResult> Get([FromRoute] int id)
        {
            var genre = await _genreService.Get(id); 
            
            return Ok(new ApiResponse<GenreResponse>
            {
                data = genre
            });
        }

        [HttpPost]
        public async Task<IActionResult> Add([FromBody] GenreRequest request)
        {
            var id = await _genreService.Add(request);
            return CreatedAtAction(
                nameof(Get),
                new { id = id });
        }

        [HttpPut("{id:int}")]
        public async Task<IActionResult> Update([FromRoute] int id, [FromBody] GenreRequest request)
        {
            await _genreService.Update(id, request);
            return Ok();
        }

        [HttpDelete("{id:int}")]
        public async Task<IActionResult> Delete([FromRoute] int id)
        {
            await _genreService.Delete(id);
            return NoContent();
        }
    }
}
