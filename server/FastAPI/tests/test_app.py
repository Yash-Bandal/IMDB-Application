import os
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from fastapi.testclient import TestClient
import jwt

from imdb_api.main import app


class ApplicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_endpoints_are_public(self) -> None:
        self.assertEqual(self.client.get("/").text, "IMDB API is running")
        self.assertEqual(self.client.get("/health").text, "healthy")

    def test_api_routes_require_bearer_authentication(self) -> None:
        response = self.client.get("/api/movies")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error": "Authentication token is required."})

    def test_valid_bearer_token_reaches_movie_service(self) -> None:
        settings = {
            "JWT_SECRET_KEY": "test-secret-key-with-at-least-thirty-two-bytes",
            "JWT_ISSUER": "test-issuer",
            "JWT_AUDIENCE": "test-audience",
        }
        now = datetime.now(timezone.utc)
        with patch.dict(os.environ, settings):
            token = jwt.encode(
                {
                    "iss": settings["JWT_ISSUER"],
                    "aud": settings["JWT_AUDIENCE"],
                    "iat": now,
                    "exp": now + timedelta(minutes=5),
                },
                settings["JWT_SECRET_KEY"],
                algorithm="HS256",
            )
            with patch("imdb_api.routers.movies.movies_service.list_movies", return_value=[]):
                response = self.client.get(
                    "/api/movies", headers={"Authorization": f"Bearer {token}"}
                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": []})

    def test_cors_preflight_does_not_require_authentication(self) -> None:
        response = self.client.options(
            "/api/movies",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
