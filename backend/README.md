# Enterprise Cybersecurity Platform - Backend

This directory contains the backend services for the Enterprise Cybersecurity Platform, built with Python, FastAPI, and PostgreSQL.

## Project Overview

The backend provides the core API functionalities, including:
- User authentication and authorization
- Dashboard data aggregation and real-time updates
- Network device management and monitoring (initially MikroTik)
- Security event logging and analysis
- Threat intelligence integration (planned)
- Vulnerability management (planned)
- Incident response workflows (planned)

Refer to the main `CybersecurityArchitecture.md` document in the project root for the complete system architecture.

## Technology Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (with SQLAlchemy 2.0 async)
- **Caching:** Redis
- **Authentication:** JWT (JSON Web Tokens)
- **Async Operations:** `asyncio`
- **Data Validation:** Pydantic
- **Migrations:** Alembic
- **Containerization:** Docker

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL server (can be run via Docker Compose)
- Redis server (can be run via Docker Compose)

## Getting Started

### 1. Clone the Repository

```bash
# If you haven't already:
git clone <your-repository-url>
cd <your-repository-url>/backend
```

### 2. Create Environment File

Make a copy of `.env.example` and name it `.env`. Update the values in `.env` with your actual configuration details.

```bash
cp .env.example .env
```

**Important:**
- For `DATABASE_URL`, ensure it points to your PostgreSQL instance. If using the provided `docker-compose.yml`, the default is `postgresql+asyncpg://postgres:yoursecurepassword@db:5432/appdb`.
- For `REDIS_HOST` and `REDIS_PORT`, if using `docker-compose.yml`, these will be `redis` and `6379` respectively.
- Generate a strong `JWT_SECRET_KEY`.
- Generate a Fernet key for `DEVICE_CREDENTIAL_ENCRYPTION_KEY` using Python:
  ```python
  from cryptography.fernet import Fernet
  print(Fernet.generate_key().decode())
  ```
  You can run this in a Python interpreter.

### 3. Build and Run with Docker Compose

This is the recommended way to run the application for development.

```bash
docker-compose up --build
```

This command will:
- Build the Docker image for the backend application.
- Start the backend service.
- Start PostgreSQL and Redis services as defined in `docker-compose.yml`.
- Apply database migrations automatically on startup (if Alembic is configured to do so, or manually as shown below).

The API will typically be available at `http://localhost:8000`.

### 4. (Optional) Manual Setup without Docker (Not Recommended for Full Setup)

If you prefer to run the application directly on your host (e.g., for specific debugging scenarios):

**a. Create a Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**b. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**c. Set up PostgreSQL and Redis:**
Ensure you have PostgreSQL and Redis instances running and accessible. Update your `.env` file accordingly.

**d. Run Database Migrations (Alembic):**
Before running the application for the first time, or after any model changes, apply database migrations:
```bash
# To generate a new migration (if you made model changes):
# alembic revision -m "create_some_tables"

# To apply migrations:
alembic upgrade head
```
*(Note: Ensure your `alembic.ini` is configured with the correct `sqlalchemy.url` pointing to your database, or that it reads from your environment variables.)*

**e. Run the FastAPI Application:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.
ReDoc documentation is available at `http://localhost:8000/redoc`.

## Project Structure

```
backend/
├── app/                    # Main application code
│   ├── __init__.py
│   ├── main.py             # FastAPI app initialization, routers
│   ├── api/                # API endpoints and dependencies
│   │   ├── __init__.py
│   │   ├── deps.py         # API dependencies (e.g., get_current_user)
│   │   └── v1/             # API version 1
│   │       ├── __init__.py     # v1 router aggregation
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── dashboard.py    # Dashboard related endpoints
│   │       ├── network_devices.py # Network device management
│   │       └── users.py        # User management endpoints
│   ├── core/               # Core components (config, security, db)
│   │   ├── __init__.py
│   │   ├── config.py       # Pydantic settings
│   │   ├── database.py     # SQLAlchemy setup
│   │   └── security.py     # Password hashing, JWT utils
│   ├── crud/               # Create, Read, Update, Delete operations
│   │   ├── __init__.py
│   │   ├── crud_user.py
│   │   ├── crud_organization.py
│   │   ├── crud_security_event.py
│   │   # ... other CRUD modules
│   ├── models/             # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── security_event.py
│   │   # ... other models
│   ├── schemas/            # Pydantic schemas for data validation & serialization
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── user.py
│   │   ├── organization.py
│   │   # ... other schemas
│   ├── services/           # Business logic and external service integrations
│   │   ├── __init__.py
│   │   ├── mikrotik_service.py
│   │   # ... other services
│   └── utils/              # Utility functions
│       ├── __init__.py
│       └── crypto.py       # Cryptographic utilities (e.g., for device credentials)
├── migrations/             # Alembic migration scripts
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/                  # Unit and integration tests (to be developed)
├── .env.example            # Example environment variables
├── .gitignore
├── Dockerfile              # Docker build instructions for the backend
├── docker-compose.yml      # Docker Compose setup for development
├── alembic.ini             # Alembic configuration
└── requirements.txt        # Python dependencies
```

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

## Next Steps (from current development phase)

- Implement credential encryption/decryption utilities in `app/utils/crypto.py`.
- Implement CRUD operations for the `NetworkDevice` model (`app/crud/crud_network_device.py`).
- Update `NetworkDevice` API endpoints to use CRUD operations for storing/retrieving devices.
- Modify `MikrotikService` to accept device credentials dynamically instead of relying on global settings.
- Ensure `get_mikrotik_service` dependency in `app/api/v1/network_devices.py` correctly fetches device details (including decrypted password) and passes them to `MikrotikService`.

## License

(Specify your project's license here, e.g., MIT, Apache 2.0) 