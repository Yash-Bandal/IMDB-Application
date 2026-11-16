using IMDB_API.Models.Filters;
using IMDB_API.Models.Requests;
using IMDB_API.Models.Responses;
using IMDB_API.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace IMDB_Controllers.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class MoviesController : ControllerBase
    {
        private readonly IMovieService _movieService;

        public MoviesController(IMovieService movieService)
        {
            _movieService = movieService;
        }

        [HttpGet]
        public async Task<IActionResult> Get([FromQuery] MovieFilter filter)
        {
            var movies = await _movieService.Get(filter);
            return Ok(new ApiResponse<IEnumerable<MovieResponse>>
            {
                data = movies
            });
        }

        [HttpGet("{id:int}")]
        public async Task<IActionResult> Get([FromRoute]int id)
        {
            var movie = await _movieService.Get(id);
            return Ok(new ApiResponse<MovieResponse>
            {
                data = movie
            });
        }

        [HttpPost]
        public async Task<IActionResult> Add([FromBody] MovieRequest request)
        {
            var id = await _movieService.Add(request);
            return CreatedAtAction(
                nameof(Get),
                new { id = id });
        }

        [HttpPut("{id:int}")]
        public async Task<IActionResult> Update([FromRoute]int id, [FromBody] MovieRequest request)
        {
            await _movieService.Update(id, request);
            return Ok();
        }

        [HttpDelete("{id:int}")]
        public async Task<IActionResult> Delete([FromRoute] int id)
        {
            await _movieService.Delete(id);
            return NoContent();
        }

        [HttpPut("{id:int}/poster")]
        public async Task<IActionResult> UpdatePoster(int id, IFormFile file)
        {
            var imageUrl = await _movieService.UpdatePoster(id, file);
            return Ok(new ApiResponse<string>
            {
                data = imageUrl
            });
        }

        [HttpPost("poster")]
        public async Task<IActionResult> UploadPoster(IFormFile file)
        {
            var imageUrl = await _movieService.UploadPoster(file);

            return Ok(new ApiResponse<string>
            {
                data = imageUrl
            });
        }
    }
}