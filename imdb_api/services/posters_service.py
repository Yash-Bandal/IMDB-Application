import logging
import os
import re
import uuid
from urllib.parse import quote

import requests

from imdb_api.config import setting
from imdb_api.errors import ApiError
from imdb_api.repositories import movies_repository
from imdb_api.services.common_service import ensure_exists
from imdb_api.utils.validation import positive_id


logger = logging.getLogger("imdb_api")


def upload_poster_to_supabase(image, folder):
    if image is None or not image.filename:
        raise ApiError("Poster image is required.")

    if not image.mimetype or not image.mimetype.startswith("image/"):
        raise ApiError("Please select a valid image file.")

    extension = os.path.splitext(image.filename)[1].lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,8}", extension):
        extension = ".img"

    filename = f"{uuid.uuid4()}{extension}"
    bucket = quote(setting("SUPABASE_BUCKET_NAME"), safe="")
    path = f"{folder}/{filename}"
    base_url = setting("SUPABASE_URL").rstrip("/")
    upload_url = f"{base_url}/storage/v1/object/{bucket}/{path}"

    headers = {
        "apikey": setting("SUPABASE_SECRET_KEY"),
        "Authorization": f"Bearer {setting('SUPABASE_SECRET_KEY')}",
        "Content-Type": image.mimetype,
    }
    response = requests.post(
        upload_url,
        data=image.stream,
        headers=headers,
        timeout=30,
    )
    if not response.ok:
        logger.error(
            "Supabase poster upload failed with HTTP %s",
            response.status_code,
        )
        raise ApiError("Unable to upload poster image.", 502)

    return f"{base_url}/storage/v1/object/public/{bucket}/{path}"


def upload_poster(image):
    return upload_poster_to_supabase(image, "movies")


def update_movie_poster(movie_id, image):
    positive_id(movie_id, "Movie Id")
    ensure_exists("Foundation.Movies", movie_id, "Movie")
    image_url = upload_poster_to_supabase(image, f"movies/{movie_id}")
    movies_repository.update_cover_image(movie_id, image_url)
    return image_url
