from typing import Any

from imdb_api.repositories.database import execute, execute_insert, query_all, query_one


def list_movie_reviews(movie_id: int) -> list[dict[str, Any]]:
    return query_all(
        "SELECT Id AS id, Message AS message, MovieId AS movieId "
        "FROM Foundation.Reviews WHERE MovieId = ?",
        (movie_id,),
    )


def get_movie_review(movie_id: int, review_id: int) -> dict[str, Any] | None:
    return query_one(
        "SELECT Id AS id, Message AS message, MovieId AS movieId "
        "FROM Foundation.Reviews WHERE Id = ? AND MovieId = ?",
        (review_id, movie_id),
    )


def list_user_reviews(user_id: int) -> list[dict[str, Any]]:
    return query_all(
        "SELECT Id AS id, Message AS message, MovieId AS movieId "
        "FROM Foundation.Reviews WHERE UserId = ?",
        (user_id,),
    )


def create_review(message: str, movie_id: int, user_id: int) -> int | None:
    return execute_insert(
        "INSERT INTO Foundation.Reviews (Message, MovieId, UserId) "
        "OUTPUT INSERTED.Id VALUES (?, ?, ?)",
        (message, movie_id, user_id),
    )


def update_review(movie_id: int, review_id: int, message: str) -> None:
    execute(
        "UPDATE Foundation.Reviews SET Message = ? WHERE Id = ? AND MovieId = ?",
        (message, review_id, movie_id),
    )


def delete_review(movie_id: int, review_id: int) -> None:
    execute(
        "DELETE FROM Foundation.Reviews WHERE Id = ? AND MovieId = ?",
        (review_id, movie_id),
    )
