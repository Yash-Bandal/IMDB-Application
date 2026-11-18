from typing import Any

from imdb_api.repositories.database import execute, execute_insert, query_all, query_one


def get_person(table: str, person_id: int) -> dict[str, Any] | None:
    return query_one(
        f"SELECT Id AS id, Name AS name, Bio AS bio, DateOfBirth AS dob, "
        f"Gender AS gender FROM {table} WHERE Id = ?",
        (person_id,),
    )


def list_people(table: str) -> list[dict[str, Any]]:
    return query_all(
        f"SELECT Id AS id, Name AS name, Bio AS bio, DateOfBirth AS dob, Gender AS gender "
        f"FROM {table}"
    )


def create_person(table: str, name: str, bio: str, dob: str, gender: str) -> int | None:
    return execute_insert(
        f"INSERT INTO {table} (Name, Bio, DateOfBirth, Gender) "
        "OUTPUT INSERTED.Id VALUES (?, ?, ?, ?)",
        (name, bio, dob, gender),
    )


def update_person(
    table: str, person_id: int, name: str, bio: str, dob: str, gender: str
) -> None:
    execute(
        f"UPDATE {table} SET Name = ?, Bio = ?, DateOfBirth = ?, Gender = ? WHERE Id = ?",
        (name, bio, dob, gender, person_id),
    )


def delete_person(table: str, person_id: int) -> None:
    execute(f"DELETE FROM {table} WHERE Id = ?", (person_id,))
