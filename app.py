import logging
import os
import re
import uuid
from datetime import date, datetime
from urllib.parse import quote

import pytds
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException


load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("imdb_api")


def setting(name, default=None):
    return os.getenv(name, default)


def required_settings():
    required = [
        "DB_SERVER",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "SUPABASE_URL",
        "SUPABASE_SECRET_KEY",
        "SUPABASE_BUCKET_NAME",
        "CORS_ALLOWED_ORIGINS",
    ]
    missing = [key for key in required if not setting(key, "").strip()]
    if missing:
        raise RuntimeError("Missing required configuration settings: " + ", ".join(missing))

    try:
        port = int(setting("DB_PORT"))
        if not 1 <= port <= 65535:
            raise ValueError
    except (TypeError, ValueError):
        raise RuntimeError("DB_PORT must be a valid TCP port between 1 and 65535.")

    if not setting("SUPABASE_URL").startswith("https://"):
        raise RuntimeError("SUPABASE_URL must be an HTTPS URL.")

    try:
        return parse_origins(setting("CORS_ALLOWED_ORIGINS"))
    except ValueError as exc:
        raise RuntimeError(str(exc)) from exc


def parse_origins(value):
    origins = [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]
    if not origins or any(not re.fullmatch(r"https?://[^/]+", origin) for origin in origins):
        raise ValueError("CORS_ALLOWED_ORIGINS must be a comma-separated list of site origins.")
    return origins


if setting("APP_ENV", "development").lower() == "development":
    cors_origins = parse_origins(setting("CORS_ALLOWED_ORIGINS", "http://localhost:5173"))
else:
    cors_origins = required_settings()


CORS(app, resources={r"/api/*": {"origins": cors_origins}}, allow_headers="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])


class ApiError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code

@app.errorhandler(ApiError)
def handle_api_error(error):
    return jsonify(error=str(error)), error.status_code

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    if isinstance(error, HTTPException):
        return error

    logger.exception("Unhandled application error")
    return jsonify(error="Internal server error"), 500
    
def get_connection():
    """Open a SQL Server connection using the pure-Python TDS driver."""
    connection_options = {
        "server": setting("DB_SERVER"),
        "port": int(setting("DB_PORT")),
        "database": setting("DB_NAME"),
        "user": setting("DB_USER"),
        "password": setting("DB_PASSWORD"),
        "timeout": 10,
        "login_timeout": 15,
    }

    # Configure TLS when a CA bundle is supplied by the database provider.
    ca_file = setting("DB_CA_FILE")
    if ca_file:
        connection_options["cafile"] = ca_file

    return pytds.connect(**connection_options)


def rows(cursor):
    names = [column[0] for column in cursor.description or []]
    result = []
    for row in cursor.fetchall():
        item = {}
        for index, name in enumerate(names):
            value = row[index]
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            item[name] = value
        result.append(item)
    return result


def query_all(sql, params=()):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        return rows(cursor)


def query_one(sql, params=()):
    result = query_all(sql, params)
    return result[0] if result else None


def execute(sql, params=()):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        affected_rows = cursor.rowcount
        connection.commit()
        return affected_rows


def scalar(sql, params=()):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return row[0] if row else None


def execute_insert(sql, params=()):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        connection.commit()
        return int(row[0]) if row else None


def body_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError("A JSON object is required.")
    return {str(key).lower(): value for key, value in data.items()}


def positive_id(value, label):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ApiError(f"{label} must be greater than zero.")
    if parsed <= 0:
        raise ApiError(f"{label} must be greater than zero.")
    return parsed


def required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ApiError(f"{label} is Empty.")
    return value.strip()


def ensure_exists(table, entity_id, label):
    if not scalar(f"SELECT COUNT(1) FROM {table} WHERE Id = %s", (entity_id,)):
        raise ApiError(f"{label} was not found.", 404)


def person_from_row(row):
    if row is None:
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "bio": row.get("bio"),
        "dob": row.get("dob"),
        "gender": row.get("gender"),
    }


def get_person(table, person_id):
    return query_one(
        f"SELECT Id AS id, Name AS name, Bio AS bio, DateOfBirth AS dob, Gender AS gender FROM {table} WHERE Id = %s",
        (person_id,),
    )


def list_people(table):
    return [person_from_row(row) for row in query_all(
        f"SELECT Id AS id, Name AS name, Bio AS bio, DateOfBirth AS dob, Gender AS gender FROM {table}"
    )]


def validate_person(data):
    name = required_text(data.get("name"), "name")
    bio = required_text(data.get("bio"), "Biography")
    gender = required_text(data.get("gender"), "Gender")
    raw_dob = data.get("dob")
    try:
        dob = date.fromisoformat(str(raw_dob)[:10])
    except (TypeError, ValueError):
        raise ApiError("Invalid Birthdate.")
    if dob > date.today():
        raise ApiError("Date of Birth cannot be in Future.")
    if not any(character.isalpha() for character in name):
        raise ApiError("Name must contain Letters.")
    return name, bio, dob, gender


def get_body_id_list(data, key, table, label):
    values = data.get(key) or []
    if not isinstance(values, list):
        raise ApiError(f"{label} must be a list.")
    ids = [positive_id(value, label) for value in values]
    if ids:
        placeholders = ",".join("%s" for _ in ids)
        found = {row["id"] for row in query_all(
            f"SELECT Id AS id FROM {table} WHERE Id IN ({placeholders})", ids
        )}
        invalid = sorted(set(ids) - found)
        if invalid:
            raise ApiError("Invalid Ids : " + ", ".join(map(str, invalid)), 404)
    return ids


def create_person(table, data):
    name, bio, dob, gender = validate_person(data)
    return execute_insert(
        f"INSERT INTO {table} (Name, Bio, DateOfBirth, Gender) OUTPUT INSERTED.Id VALUES (%s, %s, %s, %s)",
        (name, bio, dob, gender),
    )


def update_person(table, entity_id, data, label):
    ensure_exists(table, entity_id, label)
    name, bio, dob, gender = validate_person(data)
    execute(
        f"UPDATE {table} SET Name = %s, Bio = %s, DateOfBirth = %s, Gender = %s WHERE Id = %s",
        (name, bio, dob, gender, entity_id),
    )


def delete_person(table, entity_id, label):
    ensure_exists(table, entity_id, label)
    execute(f"DELETE FROM {table} WHERE Id = %s", (entity_id,))


def entity_routes(route, table, label):
    @app.get(f"/api/{route}", endpoint=f"{route}_get_all")
    def get_all():
        return jsonify(data=list_people(table))

    @app.get(f"/api/{route}/<int:entity_id>", endpoint=f"{route}_get_one")
    def get_one(entity_id):
        positive_id(entity_id, f"{label} Id")
        result = person_from_row(get_person(table, entity_id))
        if result is None:
            raise ApiError(f"{label} was not found.", 404)
        return jsonify(data=result)

    @app.post(f"/api/{route}", endpoint=f"{route}_add_one")
    def add_one():
        entity_id = create_person(table, body_json())
        return jsonify(id=entity_id), 201

    @app.put(f"/api/{route}/<int:entity_id>", endpoint=f"{route}_update_one")
    def update_one(entity_id):
        update_person(table, entity_id, body_json(), label)
        return "", 200

    @app.delete(f"/api/{route}/<int:entity_id>", endpoint=f"{route}_delete_one")
    def delete_one(entity_id):
        delete_person(table, entity_id, label)
        return "", 204


entity_routes("actors", "Foundation.Actors", "Actor")
entity_routes("producers", "Foundation.Producers", "Producer")


@app.get("/api/genres")
def get_genres():
    return jsonify(data=query_all("SELECT Id AS id, Name AS name FROM Foundation.Genres"))


@app.get("/api/genres/<int:genre_id>")
def get_genre(genre_id):
    positive_id(genre_id, "Genre Id")
    genre = query_one("SELECT Id AS id, Name AS name FROM Foundation.Genres WHERE Id = %s", (genre_id,))
    if genre is None:
        raise ApiError("Genre was not found.", 404)
    return jsonify(data=genre)


@app.post("/api/genres")
def add_genre():
    name = required_text(body_json().get("name"), "Genre Name")
    genre_id = execute_insert(
        "INSERT INTO Foundation.Genres (Name) OUTPUT INSERTED.Id VALUES (%s)", (name,)
    )
    return jsonify(id=genre_id), 201


@app.put("/api/genres/<int:genre_id>")
def update_genre(genre_id):
    positive_id(genre_id, "Genre Id")
    ensure_exists("Foundation.Genres", genre_id, "Genre")
    name = required_text(body_json().get("name"), "Genre Name")
    execute("UPDATE Foundation.Genres SET Name = %s WHERE Id = %s", (name, genre_id))
    return "", 200


@app.delete("/api/genres/<int:genre_id>")
def delete_genre(genre_id):
    positive_id(genre_id, "Genre Id")
    ensure_exists("Foundation.Genres", genre_id, "Genre")
    execute("DELETE FROM Foundation.Genres WHERE Id = %s", (genre_id,))
    return "", 204


def movie_row(movie_id):
    return query_one(
        "SELECT Id AS id, Name AS name, YearOfRelease AS yearOfRelease, Plot AS plot, CoverImage AS coverImage, ProducerId AS producerId FROM Foundation.Movies WHERE Id = %s",
        (movie_id,),
    )


def movie_response(row):
    if row is None:
        return None
    producer = person_from_row(get_person("Foundation.Producers", row["producerId"]))
    actors = [person_from_row(item) for item in query_all(
        "SELECT a.Id AS id, a.Name AS name, a.Bio AS bio, a.DateOfBirth AS dob, a.Gender AS gender "
        "FROM Foundation.Actors a INNER JOIN Foundation.Actor_Movies am ON a.Id = am.ActorId WHERE am.MovieId = %s",
        (row["id"],),
    )]
    genres = query_all(
        "SELECT g.Id AS id, g.Name AS name FROM Foundation.Genres g "
        "INNER JOIN Foundation.Genre_Movies gm ON g.Id = gm.GenreId WHERE gm.MovieId = %s",
        (row["id"],),
    )
    return {
        "id": row["id"], "name": row["name"], "yearOfRelease": row["yearOfRelease"],
        "plot": row.get("plot"), "coverImage": row.get("coverImage"),
        "producer": producer, "actors": actors, "genres": genres,
    }


def movie_responses(movie_rows):
    if not movie_rows:
        return []

    movie_ids = [row["id"] for row in movie_rows]
    producer_ids = list({row["producerId"] for row in movie_rows})

    movie_placeholders = ",".join("%s" for _ in movie_ids)
    producer_placeholders = ",".join("%s" for _ in producer_ids)

    # Fetch all producers in one query
    producers = query_all(
        f"""
        SELECT Id AS id, Name AS name, Bio AS bio,
               DateOfBirth AS dob, Gender AS gender
        FROM Foundation.Producers
        WHERE Id IN ({producer_placeholders})
        """,
        tuple(producer_ids)
    )
    producer_map = {p["id"]: person_from_row(p) for p in producers}

    # Fetch all actors associated with these movies
    actor_rows = query_all(
        f"""
        SELECT am.MovieId AS movieId,
               a.Id AS id, a.Name AS name, a.Bio AS bio,
               a.DateOfBirth AS dob, a.Gender AS gender
        FROM Foundation.Actors a
        INNER JOIN Foundation.Actor_Movies am ON a.Id = am.ActorId
        WHERE am.MovieId IN ({movie_placeholders})
        """,
        tuple(movie_ids)
    )

    # Fetch all genres associated with these movies
    genre_rows = query_all(
        f"""
        SELECT gm.MovieId AS movieId,
               g.Id AS id, g.Name AS name
        FROM Foundation.Genres g
        INNER JOIN Foundation.Genre_Movies gm ON g.Id = gm.GenreId
        WHERE gm.MovieId IN ({movie_placeholders})
        """,
        tuple(movie_ids)
    )

    # Group actors by movie
    actors_map = {}
    for actor in actor_rows:
        movie_id = actor.pop("movieId")
        actors_map.setdefault(movie_id, []).append(person_from_row(actor))

    # Group genres by movie
    genres_map = {}
    for genre in genre_rows:
        movie_id = genre.pop("movieId")
        genres_map.setdefault(movie_id, []).append(genre)

    # Build final response
    result = []

    for row in movie_rows:
        result.append({
            "id": row["id"],
            "name": row["name"],
            "yearOfRelease": row["yearOfRelease"],
            "plot": row.get("plot"),
            "coverImage": row.get("coverImage"),
            "producer": producer_map.get(row["producerId"]),
            "actors": actors_map.get(row["id"], []),
            "genres": genres_map.get(row["id"], [])
        })

    return result


def validate_movie(data):
    name = required_text(data.get("name"), "Movie Name")
    plot = required_text(data.get("plot"), "Movie Plot")
    year = positive_id(data.get("yearofrelease"), "Year of Release")
    producer_id = positive_id(data.get("producerid"), "Producer Id")

    cover_image = data.get("coverimage") or ""
    if not isinstance(cover_image, str):
        raise ApiError("Cover Image must be a string.")

    return name, year, plot, cover_image, producer_id


@app.get("/api/movies")
def get_movies():
    year = request.args.get("year", type=int)
    if request.args.get("year") is not None and (year is None or year <= 0):
        raise ApiError("Year must be greater than zero.")
    if year is None:
        found = query_all(
            "SELECT Id AS id, Name AS name, YearOfRelease AS yearOfRelease, Plot AS plot, CoverImage AS coverImage, ProducerId AS producerId FROM Foundation.Movies"
        )
    else:
        found = query_all(
            "SELECT Id AS id, Name AS name, YearOfRelease AS yearOfRelease, Plot AS plot, CoverImage AS coverImage, ProducerId AS producerId FROM Foundation.Movies WHERE YearOfRelease = %s",
            (year,),
        )
    return jsonify(data=movie_responses(found))


@app.get("/api/movies/<int:movie_id>")
def get_movie(movie_id):
    positive_id(movie_id, "Movie Id")
    movie = movie_response(movie_row(movie_id))
    if movie is None:
        raise ApiError("Movie was not found.", 404)
    return jsonify(data=movie)


def movie_ids(data):
    actors = get_body_id_list(data, "actorids", "Foundation.Actors", "Actor ID List")
    genres = get_body_id_list(data, "genreids", "Foundation.Genres", "Genre ID List")
    return actors, genres


def has_duplicate_movie(name, year, except_id=None):
    return bool(scalar(
        "SELECT COUNT(1) FROM Foundation.Movies WHERE LOWER(LTRIM(RTRIM(Name))) = LOWER(LTRIM(RTRIM(%s))) AND YearOfRelease = %s AND (%s IS NULL OR Id <> %s)",
        (name, year, except_id, except_id),
    ))


@app.post("/api/movies")
def add_movie():
    data = body_json()
    name, year, plot, cover_image, producer_id = validate_movie(data)
    if has_duplicate_movie(name, year):
        raise ApiError("A movie with this name and release year already exists.")
    ensure_exists("Foundation.Producers", producer_id, "Producer")
    actors, genres = movie_ids(data)
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "EXEC Foundation.usp_AddMovie @Name=%s, @YearOfRelease=%s, @Plot=%s, @CoverImage=%s, @ProducerId=%s, @ActorIds=%s, @GenreIds=%s",
            (name, year, plot, cover_image, producer_id, ",".join(map(str, actors)), ",".join(map(str, genres))),
        )
        while cursor.description is None:
            if not cursor.nextset():
                raise RuntimeError("Movie create procedure did not return a result set.")
        row = cursor.fetchone()
        if row is None:
            raise RuntimeError("Movie create procedure did not return the new movie ID.")
        movie_id = int(row[0])
        connection.commit()
    return jsonify(data={"id": movie_id}), 201


@app.put("/api/movies/<int:movie_id>")
def update_movie(movie_id):
    positive_id(movie_id, "Movie Id")
    if movie_row(movie_id) is None:
        raise ApiError("Movie was not found.", 404)
    data = body_json()
    name, year, plot, cover_image, producer_id = validate_movie(data)
    if has_duplicate_movie(name, year, movie_id):
        raise ApiError("A movie with this name and release year already exists.")
    ensure_exists("Foundation.Producers", producer_id, "Producer")
    actors, genres = movie_ids(data)
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "EXEC Foundation.usp_UpdateMovie @Id=%s, @Name=%s, @YearOfRelease=%s, @Plot=%s, @CoverImage=%s, @ProducerId=%s, @ActorIds=%s, @GenreIds=%s",
            (movie_id, name, year, plot, cover_image, producer_id, ",".join(map(str, actors)), ",".join(map(str, genres))),
        )
        connection.commit()
    return "", 200


@app.delete("/api/movies/<int:movie_id>")
def delete_movie(movie_id):
    positive_id(movie_id, "Movie Id")
    ensure_exists("Foundation.Movies", movie_id, "Movie")
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Foundation.Actor_Movies WHERE MovieId = %s", (movie_id,))
        cursor.execute("DELETE FROM Foundation.Genre_Movies WHERE MovieId = %s", (movie_id,))
        cursor.execute("DELETE FROM Foundation.Reviews WHERE MovieId = %s", (movie_id,))
        cursor.execute("DELETE FROM Foundation.Movies WHERE Id = %s", (movie_id,))
        connection.commit()
    return "", 204


@app.put("/api/movies/<int:movie_id>/poster")
def update_poster(movie_id):
    positive_id(movie_id, "Movie Id")
    ensure_exists("Foundation.Movies", movie_id, "Movie")
    image = request.files.get("file")
    if image is None or not image.filename:
        raise ApiError("Poster image is required.")
    if not image.mimetype or not image.mimetype.startswith("image/"):
        raise ApiError("Please select a valid image file.")
    extension = os.path.splitext(image.filename)[1].lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,8}", extension):
        extension = ".img"
    filename = f"{uuid.uuid4()}{extension}"
    bucket = quote(setting("SUPABASE_BUCKET_NAME"), safe="")
    path = f"movies/{movie_id}/{filename}"
    base_url = setting("SUPABASE_URL").rstrip("/")
    upload_url = f"{base_url}/storage/v1/object/{bucket}/{path}"
    headers = {
        "apikey": setting("SUPABASE_SECRET_KEY"),
        "Authorization": f"Bearer {setting('SUPABASE_SECRET_KEY')}",
        "Content-Type": image.mimetype,
    }
    response = requests.post(upload_url, data=image.stream, headers=headers, timeout=30)
    if not response.ok:
        logger.error("Supabase poster upload failed with HTTP %s", response.status_code)
        raise ApiError("Unable to upload poster image.", 502)
    public_url = f"{base_url}/storage/v1/object/public/{bucket}/{path}"
    execute("UPDATE Foundation.Movies SET CoverImage = %s WHERE Id = %s", (public_url, movie_id))
    return jsonify(data=public_url)


@app.get("/api/movies/<int:movie_id>/reviews")
def get_movie_reviews(movie_id):
    positive_id(movie_id, "Movie Id")
    found = query_all(
        "SELECT Id AS id, Message AS message, MovieId AS movieId FROM Foundation.Reviews WHERE MovieId = %s",
        (movie_id,),
    )
    return jsonify(data=found)


@app.get("/api/movies/<int:movie_id>/reviews/<int:review_id>")
def get_movie_review(movie_id, review_id):
    positive_id(movie_id, "Movie Id")
    positive_id(review_id, "Review Id")
    result = query_one(
        "SELECT Id AS id, Message AS message, MovieId AS movieId FROM Foundation.Reviews WHERE Id = %s AND MovieId = %s",
        (review_id, movie_id),
    )
    if result is None:
        raise ApiError("Review was not found.", 404)
    return jsonify(data=result)


@app.get("/api/users/<int:user_id>/reviews")
def get_user_reviews(user_id):
    positive_id(user_id, "User Id")
    found = query_all(
        "SELECT Id AS id, Message AS message, MovieId AS movieId FROM Foundation.Reviews WHERE UserId = %s",
        (user_id,),
    )
    return jsonify(data=found)


@app.post("/api/movies/<int:movie_id>/reviews")
def add_review(movie_id):
    positive_id(movie_id, "Movie Id")
    data = body_json()
    message = required_text(data.get("message"), "Review Message")
    user_id = positive_id(data.get("userid"), "User Id")
    ensure_exists("Foundation.Users", user_id, "User")
    review_id = execute_insert(
        "INSERT INTO Foundation.Reviews (Message, MovieId, UserId) OUTPUT INSERTED.Id VALUES (%s, %s, %s)",
        (message, movie_id, user_id),
    )
    return jsonify(id=review_id), 201


@app.put("/api/movies/<int:movie_id>/reviews/<int:review_id>")
def update_review(movie_id, review_id):
    positive_id(movie_id, "Movie Id")
    positive_id(review_id, "Review Id")
    data = body_json()
    message = required_text(data.get("message"), "Review Message")
    ensure_exists("Foundation.Reviews", review_id, "Review")
    execute(
        "UPDATE Foundation.Reviews SET Message = %s WHERE Id = %s AND MovieId = %s",
        (message, review_id, movie_id),
    )
    return "", 200


@app.delete("/api/movies/<int:movie_id>/reviews/<int:review_id>")
def delete_review(movie_id, review_id):
    positive_id(movie_id, "Movie Id")
    positive_id(review_id, "Review Id")
    ensure_exists("Foundation.Reviews", review_id, "Review")
    execute("DELETE FROM Foundation.Reviews WHERE Id = %s AND MovieId = %s", (review_id, movie_id))
    return "", 204


@app.get("/")
def root():
    return "IMDB API is running", 200


@app.get("/health")
def health():
    return "healthy", 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    if setting("APP_ENV", "development").lower() != "development":
        required_settings()
    app.run(host=setting("HOST", "0.0.0.0"), port=int(setting("PORT", "10000")))
