from flask import Blueprint, jsonify

from imdb_api.services import genres_service
from imdb_api.utils.validation import body_json


genres_blueprint = Blueprint("genres", __name__)


@genres_blueprint.get("/api/genres")
def get_genres():
    return jsonify(data=genres_service.list_genres())


@genres_blueprint.get("/api/genres/<int:genre_id>")
def get_genre(genre_id):
    return jsonify(data=genres_service.get_genre(genre_id))


@genres_blueprint.post("/api/genres")
def add_genre():
    genre_id = genres_service.create_genre(body_json())
    return jsonify(id=genre_id), 201


@genres_blueprint.put("/api/genres/<int:genre_id>")
def update_genre(genre_id):
    genres_service.update_genre(genre_id, body_json())
    return "", 200


@genres_blueprint.delete("/api/genres/<int:genre_id>")
def delete_genre(genre_id):
    genres_service.delete_genre(genre_id)
    return "", 204
