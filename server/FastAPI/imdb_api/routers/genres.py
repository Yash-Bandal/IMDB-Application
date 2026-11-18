from fastapi import APIRouter, Response

from imdb_api.schemas import GenreRequest
from imdb_api.services import genres_service

router = APIRouter()


@router.get("/genres")
def get_genres() -> dict:
    return {"data": genres_service.list_genres()}


@router.get("/genres/{genre_id}")
def get_genre(genre_id: int) -> dict:
    return {"data": genres_service.get_genre(genre_id)}


@router.post("/genres", status_code=201)
def add_genre(request: GenreRequest) -> dict:
    genre_id = genres_service.create_genre(request.model_dump(by_alias=True))
    return {"id": genre_id}


@router.put("/genres/{genre_id}")
def update_genre(genre_id: int, request: GenreRequest) -> Response:
    genres_service.update_genre(genre_id, request.model_dump(by_alias=True))
    return Response(status_code=200)


@router.delete("/genres/{genre_id}", status_code=204)
def delete_genre(genre_id: int) -> Response:
    genres_service.delete_genre(genre_id)
    return Response(status_code=204)
