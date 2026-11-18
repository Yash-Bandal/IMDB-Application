import unittest
from datetime import date, timedelta

from imdb_api.errors import ApiError
from imdb_api.schemas import MovieRequest
from imdb_api.services.validation import validate_person


class RequestSchemaTests(unittest.TestCase):
    def test_movie_accepts_frontend_and_aspnet_casing(self) -> None:
        frontend_request = MovieRequest.model_validate(
            {
                "Name": "Example",
                "yearOfRelease": 2024,
                "Plot": "A plot",
                "producerID": 3,
                "actorIds": [1],
                "GenreIDs": [2],
            }
        )
        self.assertEqual(frontend_request.year_of_release, 2024)
        self.assertEqual(frontend_request.producer_id, 3)
        self.assertEqual(frontend_request.actor_ids, [1])
        self.assertEqual(frontend_request.genre_ids, [2])

    def test_person_validation_rejects_future_birthdate(self) -> None:
        with self.assertRaisesRegex(ApiError, "Date of Birth cannot be in Future."):
            validate_person(
                {
                    "name": "Example Person",
                    "bio": "Biography",
                    "dob": (date.today() + timedelta(days=1)).isoformat(),
                    "gender": "Other",
                }
            )

    def test_person_validation_accepts_case_insensitive_keys(self) -> None:
        validated = validate_person(
            {
                "Name": "Example Person",
                "BIO": "Biography",
                "DOB": "1990-01-01",
                "Gender": "Other",
            }
        )
        self.assertEqual(validated[0], "Example Person")
        self.assertEqual(validated[1], "Biography")
        self.assertEqual(validated[2], date(1990, 1, 1))


if __name__ == "__main__":
    unittest.main()
