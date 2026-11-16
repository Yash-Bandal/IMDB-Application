import os
import re

from dotenv import load_dotenv


load_dotenv()


def setting(name, default=None):
    return os.getenv(name, default)


def parse_origins(value):
    origins = [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]
    if not origins or any(not re.fullmatch(r"https?://[^/]+", origin) for origin in origins):
        raise ValueError("CORS_ALLOWED_ORIGINS must be a comma-separated list of site origins.")
    return origins


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
        "JWT_SECRET_KEY",
        "JWT_ISSUER",
        "JWT_AUDIENCE",
        "JWT_EXPIRY_MINUTES",
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

    try:
        expiry = int(setting("JWT_EXPIRY_MINUTES"))
        if expiry <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise RuntimeError("JWT_EXPIRY_MINUTES must be a positive integer.")

    if not setting("SUPABASE_URL").startswith("https://"):
        raise RuntimeError("SUPABASE_URL must be an HTTPS URL.")

    try:
        return parse_origins(setting("CORS_ALLOWED_ORIGINS"))
    except ValueError as exc:
        raise RuntimeError(str(exc)) from exc


def cors_origins():
    if setting("APP_ENV", "development").lower() == "development":
        return parse_origins(setting("CORS_ALLOWED_ORIGINS", "http://localhost:5173"))
    return required_settings()
