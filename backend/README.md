# Enterprise Cybersecurity Platform - Backend

This directory contains the backend services for the Enterprise Cybersecurity Platform, built with Python, FastAPI, and PostgreSQL.

## Project Overview

The backend provides the core API functionalities, including:
- User authentication and authorization
- Dashboard data aggregation and real-time updates
- Network device management and monitoring (MikroTik and planned for others)
- Security event logging and analysis
- Threat intelligence integration (planned)
- Vulnerability management (planned)
- Incident response workflows (planned)

Refer to the main `CybersecurityArchitecture.md` document in the project root for the complete system architecture.

## Technology Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (with SQLAlchemy 2.0 async, using `asyncpg` driver)
- **Caching:** Redis
- **Authentication:** JWT (JSON Web Tokens)
- **Async Operations:** `asyncio`
- **Data Validation:** Pydantic (including `email-validator`)
- **Migrations:** Alembic
- **Containerization:** Docker (optional, for development environment)

## Prerequisites

- Python 3.11+
- Pip (Python package installer)
- Access to a PostgreSQL server instance.
- Access to a Redis server instance (optional for some features, required for others like WebSockets if implemented).
- Docker and Docker Compose (optional, if you prefer to run PostgreSQL and Redis via Docker for local development).

## Getting Started

### 1. Clone the Repository

```bash
# If you haven't already:
git clone <your-repository-url>
cd <your-repository-url>/backend
```

### 2. Create and Configure Environment File (`.env`)

In the `backend/` directory, create a file named `.env`.

You can copy `backend/.env.example` as a template:
```bash
cp .env.example .env
```
Then, edit the `.env` file with your actual configuration details. Key variables include:

-   `DATABASE_URL`: The connection string for your PostgreSQL database. 
    -   **Crucially, it must start with `postgresql+asyncpg://`** to use the asynchronous `asyncpg` driver.
    -   Example for a local or remote instance: `postgresql+asyncpg://user:password@host:port/dbname`
    -   If using the provided `docker-compose.yml` (and you update it for asyncpg): `postgresql+asyncpg://postgres:yoursecurepassword@db:5432/appdb`
-   `SECRET_KEY`: A strong, random string used for JWT signing and other security purposes. Generate one using `openssl rand -hex 32` or a similar method.
-   `DEVICE_CREDENTIAL_ENCRYPTION_KEY`: A Fernet key for encrypting sensitive device credentials. Generate one using the Python snippet provided in `.env.example`.
-   `REDIS_URL`: The connection string for your Redis instance (e.g., `redis://localhost:6379/0`).
-   Other variables like `PROJECT_NAME`, `API_V1_STR`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` can be reviewed and set if needed (defaults are often provided in `app/core/config.py`).

**Important:** Ensure your `.env` file is added to `.gitignore` to prevent committing secrets.

### 3. Set Up Python Virtual Environment and Install Dependencies

It's highly recommended to use a Python virtual environment.

```bash
# Navigate to the backend directory if you aren't already there
# cd backend

# Create a virtual environment (e.g., named .venv)
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell/cmd):
# .\.venv\Scripts\activate
# On macOS/Linux (bash/zsh):
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Database Migrations (Alembic)

Before running the application for the first time, or after any database model changes, apply database migrations. Ensure your virtual environment is active and you are in the `backend` directory.

```bash
alembic upgrade head
```

### 5. Run the FastAPI Application Locally

With the virtual environment active and you are in the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The application will typically be available at `http://127.0.0.1:8000`.

### (Optional) Using Docker Compose for Development Dependencies

If you prefer to run PostgreSQL and Redis in Docker containers for local development:
1.  Ensure Docker and Docker Compose are installed.
2.  Configure your `backend/.env` file to point `DATABASE_URL` and `REDIS_URL` to the services defined in `docker-compose.yml` (e.g., `db` for PostgreSQL, `redis` for Redis).
    - For `DATABASE_URL` in this case, it would be something like: `postgresql+asyncpg://postgres:yoursecurepassword@db:5432/appdb` (ensure `yoursecurepassword` matches `POSTGRES_PASSWORD` in `docker-compose.yml`).
    - For `REDIS_URL`: `redis://redis:6379/0`
3.  From the `backend/` directory, run:
    ```bash
    docker-compose up --build -d # -d to run in detached mode
    ```
4.  Then proceed with activating your local Python virtual environment, installing requirements (if not already done for local dev), running migrations against the Dockerized DB, and finally running the Uvicorn server locally (which will connect to the Dockerized DB/Redis).

## API Documentation

Once the application is running, interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.
ReDoc documentation is available at `http://127.0.0.1:8000/redoc`.

## Project Structure

```
backend/
├── app/                    # Main application code
│   ├── __init__.py
│   ├── main.py             # FastAPI app initialization, routers
│   ├── api/                # API endpoints and dependencies
│   ├── core/               # Core components (config, security, db)
│   ├── crud/               # Create, Read, Update, Delete operations
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic schemas for data validation & serialization
│   ├── services/           # Business logic and external service integrations
│   └── utils/              # Utility functions
├── migrations/             # Alembic migration scripts
├── tests/                  # Unit and integration tests (to be developed)
├── .env.example            # Example environment variables
├── .gitignore
├── Dockerfile              # Docker build instructions for the backend
├── docker-compose.yml      # Docker Compose setup for development
├── alembic.ini             # Alembic configuration
└── requirements.txt        # Python dependencies
```
(Detailed structure within subdirectories like `api`, `core`, etc., can be explored in the codebase.)

## Running Tests

(Instructions for running tests will be added here once the test suite is developed.)

```bash
# pytest
```

## Contributing

Please follow standard coding practices:
- Write clear, maintainable code.
- Add Pydantic schemas for all API request/response bodies.
- Add CRUD operations for new models.
- Ensure all new endpoints are authenticated appropriately.
- Write tests for new features and bug fixes.
- Keep `requirements.txt` updated.

## License

(Specify your project's license here, e.g., MIT, Apache 2.0) 