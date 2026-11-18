from fastapi import APIRouter, Response

from imdb_api.schemas import ReviewRequest
from imdb_api.services import reviews_service

router = APIRouter()


@router.get("/movies/{movie_id}/reviews")
def get_movie_reviews(movie_id: int) -> dict:
    return {"data": reviews_service.list_movie_reviews(movie_id)}


@router.get("/movies/{movie_id}/reviews/{review_id}")
def get_movie_review(movie_id: int, review_id: int) -> dict:
    return {"data": reviews_service.get_movie_review(movie_id, review_id)}


@router.get("/users/{user_id}/reviews")
def get_user_reviews(user_id: int) -> dict:
    return {"data": reviews_service.list_user_reviews(user_id)}


@router.post("/movies/{movie_id}/reviews", status_code=201)
def add_review(movie_id: int, request: ReviewRequest) -> dict:
    review_id = reviews_service.create_review(movie_id, request.model_dump(by_alias=True))
    return {"id": review_id}


@router.put("/movies/{movie_id}/reviews/{review_id}")
def update_review(movie_id: int, review_id: int, request: ReviewRequest) -> Response:
    reviews_service.update_review(
        movie_id, review_id, request.model_dump(by_alias=True)
    )
    return Response(status_code=200)


@router.delete("/movies/{movie_id}/reviews/{review_id}", status_code=204)
def delete_review(movie_id: int, review_id: int) -> Response:
    reviews_service.delete_review(movie_id, review_id)
    return Response(status_code=204)
