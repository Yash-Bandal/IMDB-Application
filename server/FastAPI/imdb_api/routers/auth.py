from fastapi import APIRouter

from imdb_api.schemas import LoginRequest
from imdb_api.services.auth_service import login

router = APIRouter()


@router.post("/auth/login")
def login_route(request: LoginRequest) -> dict:
    token = login(request.model_dump(by_alias=True))
    return {"data": {"accessToken": token}}
