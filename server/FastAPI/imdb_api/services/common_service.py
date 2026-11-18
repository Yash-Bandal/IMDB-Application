from imdb_api.errors import ApiError
from imdb_api.repositories.database import exists


def ensure_exists(table: str, entity_id: int, label: str) -> None:
    if not exists(table, entity_id):
        raise ApiError(f"{label} was not found.", 404)
