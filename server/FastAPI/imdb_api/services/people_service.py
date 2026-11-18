from typing import Any

from imdb_api.errors import ApiError
from imdb_api.repositories import people_repository
from imdb_api.services.common_service import ensure_exists
from imdb_api.services.validation import positive_id, validate_person


def person_from_row(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "bio": row.get("bio"),
        "dob": row.get("dob"),
        "gender": row.get("gender"),
    }


def list_people(table: str) -> list[dict[str, Any] | None]:
    return [person_from_row(row) for row in people_repository.list_people(table)]


def get_one(table: str, entity_id: int, label: str) -> dict[str, Any]:
    positive_id(entity_id, f"{label} Id")
    result = person_from_row(people_repository.get_person(table, entity_id))
    if result is None:
        raise ApiError(f"{label} was not found.", 404)
    return result


def create_person(table: str, data: dict[str, Any]) -> int | None:
    name, bio, dob, gender = validate_person(data)
    return people_repository.create_person(table, name, bio, dob, gender.isoformat())


def update_person(table: str, entity_id: int, data: dict[str, Any], label: str) -> None:
    ensure_exists(table, entity_id, label)
    name, bio, dob, gender = validate_person(data)
    people_repository.update_person(table, entity_id, name, bio, dob.isoformat(), gender)


def delete_person(table: str, entity_id: int, label: str) -> None:
    ensure_exists(table, entity_id, label)
    people_repository.delete_person(table, entity_id)
