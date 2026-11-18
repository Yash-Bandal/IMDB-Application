# FastAPI IMDB backend

This backend follows the Flask API contract and the ASP.NET SQL Server schema. The application is layered: routers handle HTTP, services contain business rules, repositories own SQL access, and schemas/configuration are kept separate.

## Run locally

From `server/FastAPI`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Fill in the SQL Server, JWT, and Supabase settings in .env.
uvicorn imdb_api.main:app --reload
```

The API listens on `http://127.0.0.1:8000`; interactive documentation is at `/docs`. The Vue client can continue using `/api/...` endpoints at this base URL. Root and `/health` are public; all other `/api` endpoints require a bearer token. Login is the only public API route.

## Configuration

Set the SQL Server connection using `DB_SERVER`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`. Optional `DB_CA_FILE` points to a CA certificate file. Set the JWT issuer, audience, secret, and expiry with the `JWT_*` variables, and set `SUPABASE_URL`, `SUPABASE_SECRET_KEY`, and `SUPABASE_BUCKET_NAME` for poster uploads. `CORS_ALLOWED_ORIGINS` is a comma-separated list of exact origins; it defaults to the Vue development origin.

Do not commit `.env` or real credentials. Poster uploads accept image files up to 8 MB.

Run the focused checks with `pip install -r requirements-dev.txt` followed by `python -m unittest discover -s tests -v`.

## API surface

- `POST /api/auth/login`
- CRUD for `/api/movies`, `/api/genres`, `/api/actors`, and `/api/producers`
- `POST /api/movies/poster` and `PUT /api/movies/{id}/poster`
- Movie and user review list/create/update/delete routes matching the Flask API

The database calls use the existing `Foundation` schema and stored procedures for movie create/update.
