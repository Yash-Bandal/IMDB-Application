from imdb_api.repositories.database import execute, execute_insert, query_all, query_one


def list_movie_reviews(movie_id):
    return query_all(
        "SELECT Id AS id, Message AS message, MovieId AS movieId FROM Foundation.Reviews WHERE MovieId = %s",
        (movie_id,),
    )


def get_movie_review(movie_id, review_id):
    return query_one(
        "SELECT Id AS id, Message AS message, MovieId AS movieId FROM Foundation.Reviews WHERE Id = %s AND MovieId = %s",
        (review_id, movie_id),
    )


def list_user_reviews(user_id):
    return query_all(
        "SELECT Id AS id, Message AS message, MovieId AS movieId FROM Foundation.Reviews WHERE UserId = %s",
        (user_id,),
    )


def create_review(message, movie_id, user_id):
    return execute_insert(
        "INSERT INTO Foundation.Reviews (Message, MovieId, UserId) OUTPUT INSERTED.Id VALUES (%s, %s, %s)",
        (message, movie_id, user_id),
    )


def update_review(movie_id, review_id, message):
    execute(
        "UPDATE Foundation.Reviews SET Message = %s WHERE Id = %s AND MovieId = %s",
        (message, review_id, movie_id),
    )


def delete_review(movie_id, review_id):
    execute(
        "DELETE FROM Foundation.Reviews WHERE Id = %s AND MovieId = %s",
        (review_id, movie_id),
    )
