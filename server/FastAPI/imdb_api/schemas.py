from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


def to_camel(value: str) -> str:
    first, *rest = value.split("_")
    return first + "".join(part.capitalize() for part in rest)


class ApiModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
    )

    @model_validator(mode="before")
    @classmethod
    def accept_case_insensitive_keys(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value

        aliases: dict[str, str] = {}
        for field_name, field in cls.model_fields.items():
            aliases[field_name.casefold()] = field_name
            if isinstance(field.alias, str):
                aliases[field.alias.casefold()] = field_name
        return {
            aliases.get(str(key).replace("_", "").casefold(), key): item
            for key, item in value.items()
        }


class MovieRequest(ApiModel):
    name: str
    year_of_release: int
    plot: str
    producer_id: int
    cover_image: str = ""
    actor_ids: list[int] = Field(default_factory=list)
    genre_ids: list[int] = Field(default_factory=list)


class PersonRequest(ApiModel):
    name: str
    bio: str
    dob: date
    gender: str


class GenreRequest(ApiModel):
    name: str


class ReviewRequest(ApiModel):
    message: str
    user_id: int


class LoginRequest(ApiModel):
    email_id: str
    password: str
