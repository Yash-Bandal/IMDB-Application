from imdb_api.repositories.database import execute, get_connection, query_all, query_one, scalar


def get_movie(movie_id):
    return query_one(
        "SELECT Id AS id, Name AS name, YearOfRelease AS yearOfRelease, Plot AS plot, CoverImage AS coverImage, ProducerId AS producerId FROM Foundation.Movies WHERE Id = %s",
        (movie_id,),
    )


def list_movies(year=None):
    sql = (
        "SELECT Id AS id, Name AS name, YearOfRelease AS yearOfRelease, Plot AS plot, "
        "CoverImage AS coverImage, ProducerId AS producerId FROM Foundation.Movies"
    )
    if year is None:
        return query_all(sql)
    return query_all(sql + " WHERE YearOfRelease = %s", (year,))


def get_movie_actors(movie_id):
    return query_all(
        "SELECT a.Id AS id, a.Name AS name, a.Bio AS bio, a.DateOfBirth AS dob, a.Gender AS gender "
        "FROM Foundation.Actors a INNER JOIN Foundation.Actor_Movies am ON a.Id = am.ActorId WHERE am.MovieId = %s",
        (movie_id,),
    )


def get_movie_genres(movie_id):
    return query_all(
        "SELECT g.Id AS id, g.Name AS name FROM Foundation.Genres g "
        "INNER JOIN Foundation.Genre_Movies gm ON g.Id = gm.GenreId WHERE gm.MovieId = %s",
        (movie_id,),
    )


def get_movie_producer(producer_id):
    return query_one(
        "SELECT Id AS id, Name AS name, Bio AS bio, DateOfBirth AS dob, Gender AS gender "
        "FROM Foundation.Producers WHERE Id = %s",
        (producer_id,),
    )


def get_movie_producers(producer_ids):
    placeholders = ",".join("%s" for _ in producer_ids)
    return query_all(
        f"""
        SELECT Id AS id, Name AS name, Bio AS bio,
               DateOfBirth AS dob, Gender AS gender
        FROM Foundation.Producers
        WHERE Id IN ({placeholders})
        """,
        tuple(producer_ids),
    )


def get_actors_for_movies(movie_ids):
    placeholders = ",".join("%s" for _ in movie_ids)
    return query_all(
        f"""
        SELECT am.MovieId AS movieId,
               a.Id AS id, a.Name AS name, a.Bio AS bio,
               a.DateOfBirth AS dob, a.Gender AS gender
        FROM Foundation.Actors a
        INNER JOIN Foundation.Actor_Movies am ON a.Id = am.ActorId
        WHERE am.MovieId IN ({placeholders})
        """,
        tuple(movie_ids),
    )


def get_genres_for_movies(movie_ids):
    placeholders = ",".join("%s" for _ in movie_ids)
    return query_all(
        f"""
        SELECT gm.MovieId AS movieId,
               g.Id AS id, g.Name AS name
        FROM Foundation.Genres g
        INNER JOIN Foundation.Genre_Movies gm ON g.Id = gm.GenreId
        WHERE gm.MovieId IN ({placeholders})
        """,
        tuple(movie_ids),
    )


def get_existing_ids(table, entity_ids):
    placeholders = ",".join("%s" for _ in entity_ids)
    return {
        row["id"]
        for row in query_all(
            f"SELECT Id AS id FROM {table} WHERE Id IN ({placeholders})",
            entity_ids,
        )
    }


def has_duplicate(name, year, except_id=None):
    return bool(scalar(
        "SELECT COUNT(1) FROM Foundation.Movies WHERE LOWER(LTRIM(RTRIM(Name))) = LOWER(LTRIM(RTRIM(%s))) AND YearOfRelease = %s AND (%s IS NULL OR Id <> %s)",
        (name, year, except_id, except_id),
    ))


def create_movie(name, year, plot, cover_image, producer_id, actor_ids, genre_ids):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "EXEC Foundation.usp_AddMovie @Name=%s, @YearOfRelease=%s, @Plot=%s, @CoverImage=%s, @ProducerId=%s, @ActorIds=%s, @GenreIds=%s",
            (
                name,
                year,
                plot,
                cover_image,
                producer_id,
                ",".join(map(str, actor_ids)),
                ",".join(map(str, genre_ids)),
            ),
        )
        while cursor.description is None:
            if not cursor.nextset():
                raise RuntimeError("Movie create procedure did not return a result set.")
        row = cursor.fetchone()
        if row is None:
            raise RuntimeError("Movie create procedure did not return the new movie ID.")
        movie_id = int(row[0])
        connection.commit()
    return movie_id


def update_movie(movie_id, name, year, plot, cover_image, producer_id, actor_ids, genre_ids):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "EXEC Foundation.usp_UpdateMovie @Id=%s, @Name=%s, @YearOfRelease=%s, @Plot=%s, @CoverImage=%s, @ProducerId=%s, @ActorIds=%s, @GenreIds=%s",
            (
                movie_id,
                name,
                year,
                plot,
                cover_image,
                producer_id,
                ",".join(map(str, actor_ids)),
                ",".join(map(str, genre_ids)),
            ),
        )
        connection.commit()


def delete_movie(movie_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Foundation.Actor_Movies WHERE MovieId = %s", (movie_id,))
        cursor.execute("DELETE FROM Foundation.Genre_Movies WHERE MovieId = %s", (movie_id,))
        cursor.execute("DELETE FROM Foundation.Reviews WHERE MovieId = %s", (movie_id,))
        cursor.execute("DELETE FROM Foundation.Movies WHERE Id = %s", (movie_id,))
        connection.commit()


def update_cover_image(movie_id, image_url):
    execute(
        "UPDATE Foundation.Movies SET CoverImage = %s WHERE Id = %s",
        (image_url, movie_id),
    )
