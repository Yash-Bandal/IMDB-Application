from imdb_api.errors import ApiError
from imdb_api.repositories import genres_repository
from imdb_api.services.common_service import ensure_exists
from imdb_api.utils.validation import positive_id, required_text


def list_genres():
    return genres_repository.list_genres()


def get_genre(genre_id):
    positive_id(genre_id, "Genre Id")
    genre = genres_repository.get_genre(genre_id)
    if genre is None:
        raise ApiError("Genre was not found.", 404)
    return genre


def create_genre(data):
    name = required_text(data.get("name"), "Genre Name")
    return genres_repository.create_genre(name)


def update_genre(genre_id, data):
    positive_id(genre_id, "Genre Id")
    ensure_exists("Foundation.Genres", genre_id, "Genre")
    name = required_text(data.get("name"), "Genre Name")
    genres_repository.update_genre(genre_id, name)


def delete_genre(genre_id):
    positive_id(genre_id, "Genre Id")
    ensure_exists("Foundation.Genres", genre_id, "Genre")
    genres_repository.delete_genre(genre_id)
