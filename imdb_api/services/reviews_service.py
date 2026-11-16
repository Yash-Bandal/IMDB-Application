from imdb_api.errors import ApiError
from imdb_api.repositories import reviews_repository
from imdb_api.services.common_service import ensure_exists
from imdb_api.utils.validation import positive_id, required_text


def list_movie_reviews(movie_id):
    positive_id(movie_id, "Movie Id")
    return reviews_repository.list_movie_reviews(movie_id)


def get_movie_review(movie_id, review_id):
    positive_id(movie_id, "Movie Id")
    positive_id(review_id, "Review Id")
    result = reviews_repository.get_movie_review(movie_id, review_id)
    if result is None:
        raise ApiError("Review was not found.", 404)
    return result


def list_user_reviews(user_id):
    positive_id(user_id, "User Id")
    return reviews_repository.list_user_reviews(user_id)


def create_review(movie_id, data):
    positive_id(movie_id, "Movie Id")
    message = required_text(data.get("message"), "Review Message")
    user_id = positive_id(data.get("userid"), "User Id")
    ensure_exists("Foundation.Users", user_id, "User")
    return reviews_repository.create_review(message, movie_id, user_id)


def update_review(movie_id, review_id, data):
    positive_id(movie_id, "Movie Id")
    positive_id(review_id, "Review Id")
    message = required_text(data.get("message"), "Review Message")
    ensure_exists("Foundation.Reviews", review_id, "Review")
    reviews_repository.update_review(movie_id, review_id, message)


def delete_review(movie_id, review_id):
    positive_id(movie_id, "Movie Id")
    positive_id(review_id, "Review Id")
    ensure_exists("Foundation.Reviews", review_id, "Review")
    reviews_repository.delete_review(movie_id, review_id)
