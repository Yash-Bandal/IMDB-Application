from imdb_api.errors import ApiError
from imdb_api.repositories.database import exists


def ensure_exists(table, entity_id, label):
    if not exists(table, entity_id):
        raise ApiError(f"{label} was not found.", 404)
