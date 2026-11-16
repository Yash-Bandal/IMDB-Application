from datetime import date

from flask import request

from imdb_api.errors import ApiError


def body_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError("A JSON object is required.")
    return {str(key).lower(): value for key, value in data.items()}


def positive_id(value, label):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ApiError(f"{label} must be greater than zero.")
    if parsed <= 0:
        raise ApiError(f"{label} must be greater than zero.")
    return parsed


def required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ApiError(f"{label} is Empty.")
    return value.strip()


def validate_person(data):
    name = required_text(data.get("name"), "name")
    bio = required_text(data.get("bio"), "Biography")
    gender = required_text(data.get("gender"), "Gender")
    raw_dob = data.get("dob")
    try:
        dob = date.fromisoformat(str(raw_dob)[:10])
    except (TypeError, ValueError):
        raise ApiError("Invalid Birthdate.")
    if dob > date.today():
        raise ApiError("Date of Birth cannot be in Future.")
    if not any(character.isalpha() for character in name):
        raise ApiError("Name must contain Letters.")
    return name, bio, dob, gender


def validate_movie(data):
    name = required_text(data.get("name"), "Movie Name")
    plot = required_text(data.get("plot"), "Movie Plot")
    year = positive_id(data.get("yearofrelease"), "Year of Release")
    producer_id = positive_id(data.get("producerid"), "Producer Id")

    cover_image = data.get("coverimage") or ""
    if not isinstance(cover_image, str):
        raise ApiError("Cover Image must be a string.")

    return name, year, plot, cover_image, producer_id

