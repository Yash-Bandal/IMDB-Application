from imdb_api.repositories.database import execute, execute_insert, query_all, query_one


def list_genres():
    return query_all("SELECT Id AS id, Name AS name FROM Foundation.Genres")


def get_genre(genre_id):
    return query_one(
        "SELECT Id AS id, Name AS name FROM Foundation.Genres WHERE Id = %s",
        (genre_id,),
    )


def create_genre(name):
    return execute_insert(
        "INSERT INTO Foundation.Genres (Name) OUTPUT INSERTED.Id VALUES (%s)",
        (name,),
    )


def update_genre(genre_id, name):
    execute(
        "UPDATE Foundation.Genres SET Name = %s WHERE Id = %s",
        (name, genre_id),
    )


def delete_genre(genre_id):
    execute("DELETE FROM Foundation.Genres WHERE Id = %s", (genre_id,))
