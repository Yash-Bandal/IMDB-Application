from fastapi import APIRouter, Query, Response

from imdb_api.schemas import MovieRequest
from imdb_api.services import movies_service
from imdb_api.services.validation import positive_id

router = APIRouter()


@router.get("/movies")
def get_movies(year: str | None = Query(default=None)) -> dict:
    parsed_year = positive_id(year, "Year") if year is not None else None
    return {"data": movies_service.list_movies(parsed_year)}


@router.get("/movies/{movie_id}")
def get_movie(movie_id: int) -> dict:
    return {"data": movies_service.get_movie(movie_id)}


@router.post("/movies", status_code=201)
def add_movie(request: MovieRequest) -> dict:
    movie_id = movies_service.create_movie(request.model_dump(by_alias=True))
    return {"id": movie_id}


@router.put("/movies/{movie_id}")
def update_movie(movie_id: int, request: MovieRequest) -> Response:
    movies_service.update_movie(movie_id, request.model_dump(by_alias=True))
    return Response(status_code=200)


@router.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int) -> Response:
    movies_service.delete_movie(movie_id)
    return Response(status_code=204)
