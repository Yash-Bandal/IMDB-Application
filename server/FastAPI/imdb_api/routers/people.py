from fastapi import APIRouter, Response

from imdb_api.schemas import PersonRequest
from imdb_api.services import people_service


def create_people_router(route: str, table: str, label: str) -> APIRouter:
    router = APIRouter()

    @router.get(f"/{route}")
    def get_all() -> dict:
        return {"data": people_service.list_people(table)}

    @router.get(f"/{route}/{{entity_id}}")
    def get_one(entity_id: int) -> dict:
        return {"data": people_service.get_one(table, entity_id, label)}

    @router.post(f"/{route}", status_code=201)
    def add_one(request: PersonRequest) -> dict:
        entity_id = people_service.create_person(table, request.model_dump(by_alias=True))
        return {"id": entity_id}

    @router.put(f"/{route}/{{entity_id}}")
    def update_one(entity_id: int, request: PersonRequest) -> Response:
        people_service.update_person(
            table, entity_id, request.model_dump(by_alias=True), label
        )
        return Response(status_code=200)

    @router.delete(f"/{route}/{{entity_id}}", status_code=204)
    def delete_one(entity_id: int) -> Response:
        people_service.delete_person(table, entity_id, label)
        return Response(status_code=204)

    return router
