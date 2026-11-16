from datetime import date, datetime

import pytds

from imdb_api.config import setting


def get_connection():
    connection_options = {
        "server": setting("DB_SERVER"),
        "port": int(setting("DB_PORT")),
        "database": setting("DB_NAME"),
        "user": setting("DB_USER"),
        "password": setting("DB_PASSWORD"),
        "timeout": 10,
        "login_timeout": 15,
    }

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


def exists(table, entity_id):
    return bool(scalar(f"SELECT COUNT(1) FROM {table} WHERE Id = %s", (entity_id,)))


def execute_insert(sql, params=()):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        connection.commit()
        return int(row[0]) if row else None
