from fastapi import APIRouter, File, UploadFile

from imdb_api.services.posters_service import MAX_POSTER_SIZE, update_movie_poster, upload_poster

router = APIRouter()


def _read_poster(file: UploadFile | None) -> tuple[str | None, str | None, bytes]:
    if file is None:
        return None, None, b""
    content = file.file.read(MAX_POSTER_SIZE + 1)
    return file.filename, file.content_type, content


@router.post("/movies/poster")
def upload_poster_route(file: UploadFile | None = File(default=None)) -> dict:
    filename, content_type, content = _read_poster(file)
    return {"data": upload_poster(filename, content_type, content)}


@router.put("/movies/{movie_id}/poster")
def update_poster_route(
    movie_id: int, file: UploadFile | None = File(default=None)
) -> dict:
    filename, content_type, content = _read_poster(file)
    image_url = update_movie_poster(movie_id, filename, content_type, content)
    return {"data": image_url}
