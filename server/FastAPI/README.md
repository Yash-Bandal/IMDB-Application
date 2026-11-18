# FastAPI IMDB backend



## Run locally

From `server/FastAPI`:

```powershell
python -m venv .venv
```
```
.\.venv\Scripts\Activate.ps1
```
```
pip install -r requirements.txt
```
Then
create .env
```
Copy-Item .env.example .env
```


 Fill in the SQL Server, JWT, and Supabase settings in .env.

Start
```
python -m uvicorn app:app --reload
```

The API listens on `http://127.0.0.1:8000`; interactive documentation is at `/docs`. The Vue client can continue using `/api/...` endpoints at this base URL. Root and `/health` are public; all other `/api` endpoints require a bearer token. Login is the only public API route.

