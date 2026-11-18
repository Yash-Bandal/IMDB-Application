from typing import Any

from imdb_api.repositories.database import execute, execute_insert, query_all, query_one


def list_genres() -> list[dict[str, Any]]:
    return query_all("SELECT Id AS id, Name AS name FROM Foundation.Genres")


def get_genre(genre_id: int) -> dict[str, Any] | None:
    return query_one(
        "SELECT Id AS id, Name AS name FROM Foundation.Genres WHERE Id = ?",
        (genre_id,),
    )


def create_genre(name: str) -> int | None:
    return execute_insert(
        "INSERT INTO Foundation.Genres (Name) OUTPUT INSERTED.Id VALUES (?)",
        (name,),
    )


def update_genre(genre_id: int, name: str) -> None:
    execute("UPDATE Foundation.Genres SET Name = ? WHERE Id = ?", (name, genre_id))


def delete_genre(genre_id: int) -> None:
    execute("DELETE FROM Foundation.Genres WHERE Id = ?", (genre_id,))
