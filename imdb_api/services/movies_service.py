from imdb_api.errors import ApiError
from imdb_api.repositories import movies_repository
from imdb_api.services.common_service import ensure_exists
from imdb_api.services.people_service import person_from_row
from imdb_api.utils.validation import positive_id, validate_movie


def get_movie(movie_id):
    positive_id(movie_id, "Movie Id")
    row = movies_repository.get_movie(movie_id)
    if row is None:
        raise ApiError("Movie was not found.", 404)

    producer = person_from_row(
        movies_repository.get_movie_producer(row["producerId"])
    )
    actors = [
        person_from_row(actor)
        for actor in movies_repository.get_movie_actors(movie_id)
    ]
    genres = movies_repository.get_movie_genres(movie_id)
    return {
        "id": row["id"],
        "name": row["name"],
        "yearOfRelease": row["yearOfRelease"],
        "plot": row.get("plot"),
        "coverImage": row.get("coverImage"),
        "producer": producer,
        "actors": actors,
        "genres": genres,
    }


def list_movies(year=None):
    found = movies_repository.list_movies(year)
    return movie_responses(found)


def movie_responses(movie_rows):
    if not movie_rows:
        return []

    movie_ids = [row["id"] for row in movie_rows]
    producer_ids = list({row["producerId"] for row in movie_rows})
    producers = movies_repository.get_movie_producers(producer_ids)
    producer_map = {p["id"]: person_from_row(p) for p in producers}

    actor_rows = movies_repository.get_actors_for_movies(movie_ids)
    genre_rows = movies_repository.get_genres_for_movies(movie_ids)

    actors_map = {}
    for actor in actor_rows:
        movie_id = actor.pop("movieId")
        actors_map.setdefault(movie_id, []).append(person_from_row(actor))

    genres_map = {}
    for genre in genre_rows:
        movie_id = genre.pop("movieId")
        genres_map.setdefault(movie_id, []).append(genre)

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "yearOfRelease": row["yearOfRelease"],
            "plot": row.get("plot"),
            "coverImage": row.get("coverImage"),
            "producer": producer_map.get(row["producerId"]),
            "actors": actors_map.get(row["id"], []),
            "genres": genres_map.get(row["id"], []),
        }
        for row in movie_rows
    ]


def _movie_values(data):
    name, year, plot, cover_image, producer_id = validate_movie(data)
    actor_ids = _get_body_id_list(data, "actorids", "Foundation.Actors", "Actor ID List")
    genre_ids = _get_body_id_list(data, "genreids", "Foundation.Genres", "Genre ID List")
    return name, year, plot, cover_image, producer_id, actor_ids, genre_ids


def _get_body_id_list(data, key, table, label):
    values = data.get(key) or []
    if not isinstance(values, list):
        raise ApiError(f"{label} must be a list.")

    ids = [positive_id(value, label) for value in values]
    if ids:
        found = movies_repository.get_existing_ids(table, ids)
        invalid = sorted(set(ids) - found)
        if invalid:
            raise ApiError("Invalid Ids : " + ", ".join(map(str, invalid)), 404)
    return ids


def create_movie(data):
    name, year, plot, cover_image, producer_id, actor_ids, genre_ids = _movie_values(data)
    if movies_repository.has_duplicate(name, year):
        raise ApiError("A movie with this name and release year already exists.")
    ensure_exists("Foundation.Producers", producer_id, "Producer")
    return movies_repository.create_movie(
        name, year, plot, cover_image, producer_id, actor_ids, genre_ids
    )


def update_movie(movie_id, data):
    positive_id(movie_id, "Movie Id")
    if movies_repository.get_movie(movie_id) is None:
        raise ApiError("Movie was not found.", 404)

    name, year, plot, cover_image, producer_id, actor_ids, genre_ids = _movie_values(data)
    if movies_repository.has_duplicate(name, year, movie_id):
        raise ApiError("A movie with this name and release year already exists.")
    ensure_exists("Foundation.Producers", producer_id, "Producer")
    movies_repository.update_movie(
        movie_id, name, year, plot, cover_image, producer_id, actor_ids, genre_ids
    )


def delete_movie(movie_id):
    positive_id(movie_id, "Movie Id")
    ensure_exists("Foundation.Movies", movie_id, "Movie")
    movies_repository.delete_movie(movie_id)
