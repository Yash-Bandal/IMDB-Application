import logging
import os
import re
import uuid
from urllib.parse import quote

import requests

from imdb_api.config import required_setting
from imdb_api.errors import ApiError
from imdb_api.repositories import movies_repository
from imdb_api.services.common_service import ensure_exists
from imdb_api.services.validation import positive_id

logger = logging.getLogger("imdb_api")
MAX_POSTER_SIZE = 8 * 1024 * 1024


def upload_poster_to_supabase(
    filename: str | None,
    content_type: str | None,
    content: bytes,
    folder: str,
) -> str:
    if not filename:
        raise ApiError("Poster image is required.")
    if not content_type or not content_type.startswith("image/"):
        raise ApiError("Please select a valid image file.")
    if len(content) > MAX_POSTER_SIZE:
        raise ApiError("Poster image must be no larger than 8 MB.")

    extension = os.path.splitext(filename)[1].lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,8}", extension):
        extension = ".img"

    supabase_url = required_setting("SUPABASE_URL").rstrip("/")
    secret = required_setting("SUPABASE_SECRET_KEY")
    bucket = quote(required_setting("SUPABASE_BUCKET_NAME"), safe="")
    path = f"{folder}/{uuid.uuid4()}{extension}"
    upload_url = f"{supabase_url}/storage/v1/object/{bucket}/{path}"
    response = requests.post(
        upload_url,
        data=content,
        headers={
            "apikey": secret,
            "Authorization": f"Bearer {secret}",
            "Content-Type": content_type,
        },
        timeout=30,
    )
    if not response.ok:
        logger.error("Supabase poster upload failed with HTTP %s", response.status_code)
        raise ApiError("Unable to upload poster image.", 502)
    return f"{supabase_url}/storage/v1/object/public/{bucket}/{path}"


def upload_poster(
    filename: str | None, content_type: str | None, content: bytes
) -> str:
    return upload_poster_to_supabase(filename, content_type, content, "movies")


def update_movie_poster(
    movie_id: int, filename: str | None, content_type: str | None, content: bytes
) -> str:
    positive_id(movie_id, "Movie Id")
    ensure_exists("Foundation.Movies", movie_id, "Movie")
    image_url = upload_poster_to_supabase(
        filename, content_type, content, f"movies/{movie_id}"
    )
    movies_repository.update_cover_image(movie_id, image_url)
    return image_url
