import os
import re

from dotenv import load_dotenv

load_dotenv()


def setting(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def required_setting(name: str) -> str:
    value = setting(name, "")
    if not value or not value.strip():
        raise RuntimeError(f"Missing required configuration setting: {name}")
    return value.strip()


def cors_origins() -> list[str]:
    raw_origins = setting("CORS_ALLOWED_ORIGINS", "http://localhost:5173") or ""
    origins = [origin.strip().rstrip("/") for origin in raw_origins.split(",") if origin.strip()]
    if not origins or any(not re.fullmatch(r"https?://[^/]+", origin) for origin in origins):
        raise RuntimeError(
            "CORS_ALLOWED_ORIGINS must be a comma-separated list of site origins."
        )
    return origins


def database_settings() -> str:
    server = required_setting("DB_SERVER")
    database = required_setting("DB_NAME")

    return (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

# def database_settings() -> str:
#     server = required_setting("DB_SERVER")
#     database = required_setting("DB_NAME")

#     auth_mode = setting("DB_AUTH", "sql").lower()

#     if auth_mode == "windows":
#         return (
#             "DRIVER={ODBC Driver 18 for SQL Server};"
#             f"SERVER={server};"
#             f"DATABASE={database};"
#             "Trusted_Connection=yes;"
#             "TrustServerCertificate=yes;"
#         )

#     elif auth_mode == "sql":
#         user = required_setting("DB_USER")
#         password = required_setting("DB_PASSWORD")
#         port = setting("DB_PORT", "1433")

#         return (
#             "DRIVER={ODBC Driver 18 for SQL Server};"
#             f"SERVER={server},{port};"
#             f"DATABASE={database};"
#             f"UID={user};"
#             f"PWD={password};"
#             "Encrypt=yes;"
#             "TrustServerCertificate=yes;"
#             "Connection Timeout=15;"
#         )

#     else:
#         raise RuntimeError(
#             "DB_AUTH must be either 'windows' or 'sql'."
#         )
    
def jwt_validation_settings() -> tuple[str, str, str]:
    secret = required_setting("JWT_SECRET_KEY")
    issuer = required_setting("JWT_ISSUER")
    audience = required_setting("JWT_AUDIENCE")
    return secret, issuer, audience


def jwt_settings() -> tuple[str, str, str, int]:
    secret, issuer, audience = jwt_validation_settings()
    raw_expiry = required_setting("JWT_EXPIRY_MINUTES")
    try:
        expiry = int(raw_expiry)
    except ValueError as exc:
        raise RuntimeError("JWT_EXPIRY_MINUTES must be a positive integer.") from exc
    if expiry <= 0:
        raise RuntimeError("JWT_EXPIRY_MINUTES must be a positive integer.")
    return secret, issuer, audience, expiry
