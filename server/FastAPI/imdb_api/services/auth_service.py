from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from imdb_api.config import jwt_settings
from imdb_api.errors import ApiError
from imdb_api.repositories.users_repository import get_by_email
from imdb_api.services.validation import normalize_body, required_text, validate_email


def create_access_token(user: dict[str, Any]) -> str:
    secret, issuer, audience, expiry_minutes = jwt_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "nameid": str(user["id"]),
        "email": user["email"],
        "iss": issuer,
        "aud": audience,
        "iat": now,
        "exp": now + timedelta(minutes=expiry_minutes),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def login(data: dict[str, Any]) -> str:
    fields = normalize_body(data)
    email = required_text(fields.get("emailid"), "Email Id")
    password = required_text(fields.get("password"), "Password")
    validate_email(email)

    user = get_by_email(email)
    if user is None or user["password"] != password:
        raise ApiError("Invalid credentials.", 401)
    return create_access_token(user)
