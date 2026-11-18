from datetime import date, datetime
from typing import Any, Sequence

import pyodbc

from imdb_api.config import database_settings


def get_connection() -> Any:
    return pyodbc.connect(database_settings())


def _rows(cursor: Any) -> list[dict[str, Any]]:
    names = [column[0] for column in cursor.description or []]

    result: list[dict[str, Any]] = []

    for row in cursor.fetchall():
        result.append(
            {
                name: value.isoformat()
                if isinstance(value, (datetime, date))
                else value
                for name, value in zip(names, row)
            }
        )

    return result


def query_all(sql: str, params: Sequence[Any] = ()) -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        return _rows(cursor)


def query_one(sql: str, params: Sequence[Any] = ()) -> dict[str, Any] | None:
    result = query_all(sql, params)
    return result[0] if result else None


def execute(sql: str, params: Sequence[Any] = ()) -> int:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)

        affected_rows = cursor.rowcount
        connection.commit()

        return affected_rows


def scalar(sql: str, params: Sequence[Any] = ()) -> Any:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)

        row = cursor.fetchone()

        return row[0] if row else None


def exists(table: str, entity_id: int) -> bool:
    return bool(
        scalar(
            f"SELECT COUNT(1) FROM {table} WHERE Id = ?",
            (entity_id,),
        )
    )


def execute_insert(sql: str, params: Sequence[Any] = ()) -> int | None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)

        row = cursor.fetchone()
        connection.commit()

        return int(row[0]) if row else None