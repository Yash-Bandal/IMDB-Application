# Flask API on Render

The API deploys on Render's native Python runtime. `build.sh` installs Microsoft's ODBC Driver 18 for Debian 12, installs the Python dependencies, and verifies that the driver is available before the service starts. `apt.txt` provides the required ODBC system libraries and installer utilities. Docker is not used.

## Render

Create a Blueprint from the repository root using `render.yaml`, or create a native Python web service with:

- Root directory: `server`
- Build command: `bash build.sh`
- Start command: `gunicorn --workers 2 --bind 0.0.0.0:$PORT app:app`
- Health check path: `/health`

Provide the database, Supabase, and CORS values marked `sync: false` on the Render service's Environment page:

- `DATABASE_CONNECTION_STRING`: an ODBC Driver 18 connection string for a SQL Server database reachable from Render. Example format: `Driver={ODBC Driver 18 for SQL Server};Server=tcp:HOST,1433;Database=DB;Uid=USER;Pwd=PASSWORD;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;`
- `SUPABASE_URL`: the HTTPS URL of the Supabase project.
- `SUPABASE_SECRET_KEY`: a Supabase secret key that can upload objects to the poster bucket.
- `CORS_ALLOWED_ORIGINS`: the deployed Vue site's exact origin, including `https://` and without a path. Separate multiple origins with commas.

Set `DATABASE_CONNECTION_STRING` in Render to a SQL Server that is reachable over the network and accepts SQL credentials. The legacy development connection uses Windows integrated authentication and a machine-local server name; it can work on the development machine but cannot be used by Render's Debian service.

For local development, the API reads database and Supabase settings from the existing .NET `appsettings.json` files when present; environment variables and `.env` values take precedence. Run `python app.py` locally, or use Gunicorn on Linux. Render injects `PORT`; Gunicorn binds to `0.0.0.0:$PORT`.

Render provides `PORT`; Gunicorn binds to that port. The `/health` endpoint is a simple process health check and does not depend on SQL Server.

All API routes are accessible without a JWT bearer token. PyJWT remains installed, but JWT configuration is optional and is only needed if the legacy signup/login routes are used. Since the existing SQL schema requires a review `UserId`, creating a review also requires a valid `userId` in the JSON body.

## Local development

Copy `.env.example` to `.env`, then replace the placeholders with working credentials. Install the matching system ODBC Driver 18, then run:

```powershell
cd server
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Existing users

The Flask API hashes passwords for new accounts. On successful login, it also upgrades a matching plaintext password from the previous API to a hash. The hash format is kept compact to fit typical SQL `Password` columns; if signup reports a database truncation error, widen `Foundation.Users.Password` to `NVARCHAR(255)` before retrying.

Rotate any database password, Supabase key, or JWT signing key that appeared in prior configuration or Git commits. Removing those values from current files does not erase them from the Git history.
