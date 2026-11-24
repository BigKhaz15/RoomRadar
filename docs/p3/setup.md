# RoomRadar Development Setup

## Current implementation

The starter serves a browser page and an API health endpoint.
Room browsing, reporting and PostgreSQL integration are not implemented yet.

## Prerequisites

- Git
- Standard Python 3.12
- An editor such as VS Code
- A modern browser

The Windows environment used during initial setup was Python 3.12.6.
Use the Python launcher explicitly to avoid selecting MSYS2 Python.

## Clone and select your branch

```powershell
git clone https://github.com/BigKhaz15/RoomRadar.git
cd RoomRadar
git fetch origin
```

Switch to your assigned P3 branch. For example:

```powershell
git switch p3/tien
```

If it does not exist locally or remotely, create it from updated main:

```powershell
git switch main
git pull origin main
git switch -c p3/tien
git push -u origin p3/tien
```

Replace p3/tien with your assigned branch.

The starter is initially on p3/adam. Teammates should follow the run steps
after the foundation is merged into main and incorporated into their branches.

## Create the environment — Windows PowerShell

Run these commands from the repository root:

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

Activation is not required because the commands use the environment directly.

Never commit .venv or credentials.

## Run — Windows PowerShell

```powershell
& ".\.venv\Scripts\python.exe" -m uvicorn roomradar.main:app --app-dir src --reload
```

Open:
- Browser page: http://127.0.0.1:8000/
- API health: http://127.0.0.1:8000/health
- API documentation: http://127.0.0.1:8000/docs

Expected health response:

```json
{"status":"ok"}
```

The health response confirms the API is running. It does not check database readiness.

Stop the server with Ctrl+C.

## macOS/Linux equivalent

These commands have not yet been independently verified:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn roomradar.main:app --app-dir src --reload
```

## Update your branch after shared work is merged

Commit your current work before updating. Then:

```powershell
git fetch origin
git merge origin/main
```

If Git reports conflicts you do not understand, ask for help.
Do not blindly accept one version or discard changes.

## Testing and database setup

Automated test commands and PostgreSQL configuration will be added when
those components are implemented. No database is required for this starter.

## Independent verification

The final clean-clone check is assigned to Jeimy.
Her actual commands, environment, results and any failures will be recorded
under docs/p3/evidence/clean-clone/ and included in Appendix B.

## Database configuration agreement

The application will use PostgreSQL.

- DATABASE_URL identifies the development database.
- TEST_DATABASE_URL identifies a separate test database.
- Tests must never reset or clear the development database.
- Connection handling, schema initialization and seed commands are owned by Roshan.
- Shared database fixtures and safety checks are coordinated with Malak.

.env.example documents the variable names. The application does not yet
automatically load .env files.

For Windows PowerShell, set configuration in the same terminal used to
start the server:

```powershell
$env:DATABASE_URL = "postgresql://roomradar:YOUR_LOCAL_PASSWORD@localhost:5432/roomradar"
```

Replace the example with your actual local connection details.
Do not paste real credentials into issues, screenshots or committed files.

The variable lasts for that terminal session.
Passwords containing URL-reserved characters require URL encoding.

The starter browser page and /health do not require a database.
Database-dependent features will require a running PostgreSQL instance.
PostgreSQL installation, initialization and test commands are still pending
Roshan's implementation and review.