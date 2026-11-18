import re
from datetime import date
from typing import Any

from imdb_api.errors import ApiError


def normalize_body(data: dict[str, Any]) -> dict[str, Any]:
    return {
        str(key).replace("_", "").casefold(): value
        for key, value in data.items()
    }


def positive_id(value: Any, label: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ApiError(f"{label} must be greater than zero.") from exc
    if parsed <= 0:
        raise ApiError(f"{label} must be greater than zero.")
    return parsed


def required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ApiError(f"{label} is Empty.")
    return value.strip()


def validate_person(data: dict[str, Any]) -> tuple[str, str, date, str]:
    fields = normalize_body(data)
    name = required_text(fields.get("name"), "name")
    bio = required_text(fields.get("bio"), "Biography")
    gender = required_text(fields.get("gender"), "Gender")
    raw_dob = fields.get("dob")
    try:
        dob = date.fromisoformat(str(raw_dob)[:10])
    except (TypeError, ValueError) as exc:
        raise ApiError("Invalid Birthdate.") from exc
    if dob > date.today():
        raise ApiError("Date of Birth cannot be in Future.")
    if not any(character.isalpha() for character in name):
        raise ApiError("Name must contain Letters.")
    return name, bio, dob, gender


def validate_movie(data: dict[str, Any]) -> tuple[str, int, str, str, int]:
    fields = normalize_body(data)
    name = required_text(fields.get("name"), "Movie Name")
    plot = required_text(fields.get("plot"), "Movie Plot")
    year = positive_id(fields.get("yearofrelease"), "Year of Release")
    producer_id = positive_id(fields.get("producerid"), "Producer Id")
    cover_image = fields.get("coverimage") or ""
    if not isinstance(cover_image, str):
        raise ApiError("Cover Image must be a string.")
    return name, year, plot, cover_image, producer_id


def validate_email(email: str) -> None:
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ApiError("Invalid Email Id.")
