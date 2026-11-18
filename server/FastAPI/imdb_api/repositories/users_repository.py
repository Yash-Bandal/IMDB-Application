from typing import Any

from imdb_api.repositories.database import query_one


def get_by_email(email: str) -> dict[str, Any] | None:
    return query_one(
        "SELECT Id AS id, Name AS name, Email AS email, Password AS password "
        "FROM Foundation.Users WHERE Email = ?",
        (email,),
    )
