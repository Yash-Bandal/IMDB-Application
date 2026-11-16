from flask import Blueprint, jsonify, request

from imdb_api.services.posters_service import update_movie_poster, upload_poster


posters_blueprint = Blueprint("posters", __name__)


@posters_blueprint.post("/api/movies/poster")
def upload_poster_route():
    image_url = upload_poster(request.files.get("file"))
    return jsonify(data=image_url)


@posters_blueprint.put("/api/movies/<int:movie_id>/poster")
def update_poster_route(movie_id):
    image_url = update_movie_poster(movie_id, request.files.get("file"))
    return jsonify(data=image_url)
