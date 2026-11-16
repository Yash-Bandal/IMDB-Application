import re
from datetime import datetime, timedelta, timezone

import jwt

from imdb_api.config import setting
from imdb_api.errors import ApiError
from imdb_api.repositories.users_repository import get_by_email


def create_access_token(user):
    now = datetime.now(timezone.utc)
    payload = {
        "nameid": str(user["id"]),
        "email": user["email"],
        "iss": setting("JWT_ISSUER"),
        "aud": setting("JWT_AUDIENCE"),
        "iat": now,
        "exp": now + timedelta(minutes=int(setting("JWT_EXPIRY_MINUTES"))),
    }
    return jwt.encode(payload, setting("JWT_SECRET_KEY"), algorithm="HS256")


def login(email, password):
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ApiError("Invalid Email Id.")

    user = get_by_email(email)
    if user is None or user["password"] != password:
        raise ApiError("Invalid credentials.", 401)

    return create_access_token(user)
