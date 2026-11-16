from flask import Blueprint, jsonify

from imdb_api.services import reviews_service
from imdb_api.utils.validation import body_json


reviews_blueprint = Blueprint("reviews", __name__)


@reviews_blueprint.get("/api/movies/<int:movie_id>/reviews")
def get_movie_reviews(movie_id):
    return jsonify(data=reviews_service.list_movie_reviews(movie_id))


@reviews_blueprint.get("/api/movies/<int:movie_id>/reviews/<int:review_id>")
def get_movie_review(movie_id, review_id):
    return jsonify(data=reviews_service.get_movie_review(movie_id, review_id))


@reviews_blueprint.get("/api/users/<int:user_id>/reviews")
def get_user_reviews(user_id):
    return jsonify(data=reviews_service.list_user_reviews(user_id))


@reviews_blueprint.post("/api/movies/<int:movie_id>/reviews")
def add_review(movie_id):
    review_id = reviews_service.create_review(movie_id, body_json())
    return jsonify(id=review_id), 201


@reviews_blueprint.put("/api/movies/<int:movie_id>/reviews/<int:review_id>")
def update_review(movie_id, review_id):
    reviews_service.update_review(movie_id, review_id, body_json())
    return "", 200


@reviews_blueprint.delete("/api/movies/<int:movie_id>/reviews/<int:review_id>")
def delete_review(movie_id, review_id):
    reviews_service.delete_review(movie_id, review_id)
    return "", 204
