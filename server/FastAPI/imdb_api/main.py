import logging

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from imdb_api.config import cors_origins, setting
from imdb_api.dependencies import require_auth
from imdb_api.errors import register_error_handlers
from imdb_api.routers import auth, genres, movies, posters, reviews
from imdb_api.routers.people import create_people_router

logging.basicConfig(level=setting("LOG_LEVEL", "INFO"))

app = FastAPI(title="IMDB API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
register_error_handlers(app)

protected_api = APIRouter(prefix="/api", dependencies=[Depends(require_auth)])
protected_api.include_router(movies.router)
protected_api.include_router(genres.router)
protected_api.include_router(create_people_router("actors", "Foundation.Actors", "Actor"))
protected_api.include_router(
    create_people_router("producers", "Foundation.Producers", "Producer")
)
protected_api.include_router(reviews.router)
protected_api.include_router(posters.router)
app.include_router(protected_api)

public_api = APIRouter(prefix="/api")
public_api.include_router(auth.router)
app.include_router(public_api)


@app.get("/")
def root() -> PlainTextResponse:
    return PlainTextResponse("IMDB API is running")


@app.get("/health")
def health() -> PlainTextResponse:
    return PlainTextResponse("healthy")
