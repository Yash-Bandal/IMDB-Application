from imdb_api.repositories.database import execute, execute_insert, query_all, query_one


def get_person(table, person_id):
    return query_one(
        f"SELECT Id AS id, Name AS name, Bio AS bio, DateOfBirth AS dob, Gender AS gender FROM {table} WHERE Id = %s",
        (person_id,),
    )


def list_people(table):
    return query_all(
        f"SELECT Id AS id, Name AS name, Bio AS bio, DateOfBirth AS dob, Gender AS gender FROM {table}"
    )


def create_person(table, name, bio, dob, gender):
    return execute_insert(
        f"INSERT INTO {table} (Name, Bio, DateOfBirth, Gender) OUTPUT INSERTED.Id VALUES (%s, %s, %s, %s)",
        (name, bio, dob, gender),
    )


def update_person(table, entity_id, name, bio, dob, gender):
    execute(
        f"UPDATE {table} SET Name = %s, Bio = %s, DateOfBirth = %s, Gender = %s WHERE Id = %s",
        (name, bio, dob, gender, entity_id),
    )


def delete_person(table, entity_id):
    execute(f"DELETE FROM {table} WHERE Id = %s", (entity_id,))
