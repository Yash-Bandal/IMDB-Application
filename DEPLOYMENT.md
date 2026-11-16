# Flask API on Render

The API uses Render's native Python runtime and `python-tds`, a pure-Python SQL Server driver installed with pip. It needs no Docker, root access, system packages, or Microsoft ODBC Driver.

## Render

Create a Blueprint from the repository root using `render.yaml`, or create a native Python web service with:

- Root directory: `server`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --workers 2 --bind 0.0.0.0:$PORT app:app`
- Health check path: `/health`

Set these service environment variables:

- `DATABASE_CONNECTION_STRING`: a SQL Server connection string for a server reachable from Render. Example format: `Server=tcp:HOST,1433;Database=DB;Uid=USER;Pwd=PASSWORD;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;`
- `SUPABASE_URL`: the HTTPS URL of the Supabase project.
- `SUPABASE_SECRET_KEY`: a Supabase secret key that can upload objects to the poster bucket.
- `CORS_ALLOWED_ORIGINS`: the deployed Vue site's exact origin, including `https://` and without a path. Separate multiple origins with commas.

The connection string must use SQL credentials and a network-reachable SQL Server. The legacy development connection uses Windows integrated authentication and a machine-local server name; it works on the development machine but cannot be used by Render.

For `Encrypt=yes`, the SQL Server certificate must chain to a trusted CA. If the server uses a private CA, provide its PEM certificate bundle as a Render secret file and set `DATABASE_CA_FILE` to that file's path. `TrustServerCertificate=yes` encrypts the connection but disables server-certificate verification; prefer `no` with a valid certificate.

For local development, the API reads database and Supabase settings from the existing .NET `appsettings.json` files when present; environment variables and `.env` values take precedence. Copy `.env.example` to `.env` and replace its placeholders. Install dependencies with `pip install -r requirements.txt`, then run `python app.py`. Render injects `PORT`; Gunicorn binds to `0.0.0.0:$PORT`.

## Code structure

The Flask entry point remains `app.py` so local startup and the `app:app` Gunicorn target continue to work. Application code lives in `imdb_api/`, organized into controllers for HTTP routes, services for application logic, repositories for SQL access, plus shared configuration, errors, and validation.

The `/health` endpoint is a process health check and does not depend on SQL Server.

All API routes are accessible without a JWT bearer token. PyJWT remains installed, but JWT configuration is optional and is only needed if the legacy signup/login routes are used. Since the existing SQL schema requires a review `UserId`, creating a review also requires a valid `userId` in the JSON body.

## Existing users

The Flask API hashes passwords for new accounts. On successful login, it also upgrades a matching plaintext password from the previous API to a hash. The hash format is kept compact to fit typical SQL `Password` columns; if signup reports a database truncation error, widen `Foundation.Users.Password` to `NVARCHAR(255)` before retrying.

Rotate any database password, Supabase key, or JWT signing key that appeared in prior configuration or Git commits. Removing those values from current files does not erase them from the Git history.
