from flask import Blueprint, jsonify

from imdb_api.services import people_service
from imdb_api.utils.validation import body_json


def create_people_blueprint(route, table, label):
    blueprint = Blueprint(route, __name__)

    @blueprint.get(f"/api/{route}")
    def get_all():
        return jsonify(data=people_service.list_people(table))

    @blueprint.get(f"/api/{route}/<int:entity_id>")
    def get_one(entity_id):
        return jsonify(data=people_service.get_one(table, entity_id, label))

    @blueprint.post(f"/api/{route}")
    def add_one():
        entity_id = people_service.create_person(table, body_json())
        return jsonify(id=entity_id), 201

    @blueprint.put(f"/api/{route}/<int:entity_id>")
    def update_one(entity_id):
        people_service.update_person(table, entity_id, body_json(), label)
        return "", 200

    @blueprint.delete(f"/api/{route}/<int:entity_id>")
    def delete_one(entity_id):
        people_service.delete_person(table, entity_id, label)
        return "", 204

    return blueprint
