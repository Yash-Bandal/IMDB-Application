from typing import Any

from imdb_api.errors import ApiError
from imdb_api.repositories import genres_repository
from imdb_api.services.common_service import ensure_exists
from imdb_api.services.validation import normalize_body, positive_id, required_text


def list_genres() -> list[dict[str, Any]]:
    return genres_repository.list_genres()


def get_genre(genre_id: int) -> dict[str, Any]:
    positive_id(genre_id, "Genre Id")
    genre = genres_repository.get_genre(genre_id)
    if genre is None:
        raise ApiError("Genre was not found.", 404)
    return genre


def create_genre(data: dict[str, Any]) -> int | None:
    name = required_text(normalize_body(data).get("name"), "Genre Name")
    return genres_repository.create_genre(name)


def update_genre(genre_id: int, data: dict[str, Any]) -> None:
    positive_id(genre_id, "Genre Id")
    ensure_exists("Foundation.Genres", genre_id, "Genre")
    name = required_text(normalize_body(data).get("name"), "Genre Name")
    genres_repository.update_genre(genre_id, name)


def delete_genre(genre_id: int) -> None:
    positive_id(genre_id, "Genre Id")
    ensure_exists("Foundation.Genres", genre_id, "Genre")
    genres_repository.delete_genre(genre_id)
