from typing import Any

from imdb_api.errors import ApiError
from imdb_api.repositories import movies_repository
from imdb_api.services.common_service import ensure_exists
from imdb_api.services.people_service import person_from_row
from imdb_api.services.validation import normalize_body, positive_id, validate_movie


def get_movie(movie_id: int) -> dict[str, Any]:
    positive_id(movie_id, "Movie Id")
    row = movies_repository.get_movie(movie_id)
    if row is None:
        raise ApiError("Movie was not found.", 404)

    return {
        "id": row["id"],
        "name": row["name"],
        "yearOfRelease": row["yearOfRelease"],
        "plot": row.get("plot"),
        "coverImage": row.get("coverImage"),
        "producer": person_from_row(movies_repository.get_movie_producer(row["producerId"])),
        "actors": [
            person_from_row(actor) for actor in movies_repository.get_movie_actors(movie_id)
        ],
        "genres": movies_repository.get_movie_genres(movie_id),
    }


def list_movies(year: int | None = None) -> list[dict[str, Any]]:
    return movie_responses(movies_repository.list_movies(year))


def movie_responses(movie_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not movie_rows:
        return []

    movie_ids = [row["id"] for row in movie_rows]
    producer_ids = list({row["producerId"] for row in movie_rows})
    producer_map = {
        person["id"]: person_from_row(person)
        for person in movies_repository.get_movie_producers(producer_ids)
    }

    actors_by_movie: dict[int, list[dict[str, Any] | None]] = {}
    for actor in movies_repository.get_actors_for_movies(movie_ids):
        movie_id = actor.pop("movieId")
        actors_by_movie.setdefault(movie_id, []).append(person_from_row(actor))

    genres_by_movie: dict[int, list[dict[str, Any]]] = {}
    for genre in movies_repository.get_genres_for_movies(movie_ids):
        movie_id = genre.pop("movieId")
        genres_by_movie.setdefault(movie_id, []).append(genre)

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "yearOfRelease": row["yearOfRelease"],
            "plot": row.get("plot"),
            "coverImage": row.get("coverImage"),
            "producer": producer_map.get(row["producerId"]),
            "actors": actors_by_movie.get(row["id"], []),
            "genres": genres_by_movie.get(row["id"], []),
        }
        for row in movie_rows
    ]


def _movie_values(data: dict[str, Any]) -> tuple[str, int, str, str, int, list[int], list[int]]:
    name, year, plot, cover_image, producer_id = validate_movie(data)
    fields = normalize_body(data)
    actor_ids = _body_id_list(fields.get("actorids"), "Foundation.Actors", "Actor ID List")
    genre_ids = _body_id_list(fields.get("genreids"), "Foundation.Genres", "Genre ID List")
    return name, year, plot, cover_image, producer_id, actor_ids, genre_ids


def _body_id_list(value: Any, table: str, label: str) -> list[int]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ApiError(f"{label} must be a list.")
    ids = [positive_id(item, label) for item in value]
    if ids:
        found = movies_repository.get_existing_ids(table, ids)
        invalid = sorted(set(ids) - found)
        if invalid:
            raise ApiError("Invalid Ids : " + ", ".join(map(str, invalid)), 404)
    return ids


def create_movie(data: dict[str, Any]) -> int | None:
    values = _movie_values(data)
    name, year, *_ = values
    producer_id = values[4]
    if movies_repository.has_duplicate(name, year):
        raise ApiError("A movie with this name and release year already exists.")
    ensure_exists("Foundation.Producers", producer_id, "Producer")
    return movies_repository.create_movie(*values)


def update_movie(movie_id: int, data: dict[str, Any]) -> None:
    positive_id(movie_id, "Movie Id")
    if movies_repository.get_movie(movie_id) is None:
        raise ApiError("Movie was not found.", 404)

    values = _movie_values(data)
    name, year, *_ = values
    producer_id = values[4]
    if movies_repository.has_duplicate(name, year, movie_id):
        raise ApiError("A movie with this name and release year already exists.")
    ensure_exists("Foundation.Producers", producer_id, "Producer")
    movies_repository.update_movie(movie_id, *values)


def delete_movie(movie_id: int) -> None:
    positive_id(movie_id, "Movie Id")
    ensure_exists("Foundation.Movies", movie_id, "Movie")
    movies_repository.delete_movie(movie_id)
