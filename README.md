# StudySync - AI-Powered Student Study & Performance Platform

StudySync is a FastAPI-based backend platform designed to help students manage their study activities and academic performance.

The backend currently provides user management, JWT authentication, task search and filtering, study-tip service integration, structured error handling, automated testing, and dependency-aware health checks.

---

## Tech Stack

- Python 3.14+
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- asyncpg
- Alembic
- Pydantic
- JWT Authentication
- pwdlib
- HTTPX
- Pytest

---

## Project Structure

```text
StudySync/
|
+-- alembic/
|   +-- versions/
|
+-- app/
|   +-- db/
|   +-- schemas/
|   +-- services/
|   +-- auth.py
|   +-- dependencies.py
|   +-- security.py
|   +-- main.py
|
+-- docs/
|   +-- api-design.md
|
+-- tests/
|   +-- conftest.py
|   +-- test_api_workflows.py
|   +-- test_authorization.py
|   +-- test_database.py
|   +-- test_study_tip.py
|
+-- .env
+-- .gitignore
+-- alembic.ini
+-- pytest.ini
+-- requirements.txt
+-- README.md
# Deployment Readiness

## Production Startup

For production deployment, run the FastAPI application without development reload mode.

Production startup command:
uvicorn app.main:app --host 0.0.0.0 --port 8000

The --reload option is intended for development and should not be used in production.

## Health Check

The application provides a dependency-aware health endpoint.

Endpoint:
GET /health

A healthy response confirms that the application can connect to PostgreSQL.

Healthy response:
{
  "status": "healthy",
  "message": "StudySync backend is running",
  "database": "connected"
}

If the database is unavailable, the health response reports:

{
  "status": "unhealthy",
  "message": "StudySync backend is running",
  "database": "unavailable"
}

## Deployment Checklist

- [ ] Configure production environment variables.
- [ ] Keep JWT_SECRET_KEY secure and out of source control.
- [ ] Keep .env excluded from Git.
- [ ] Configure the production PostgreSQL database.
- [ ] Apply the latest Alembic migrations.
- [ ] Verify the /health endpoint.
- [ ] Confirm database connectivity.
- [ ] Run the automated test suite.
- [ ] Start the application without --reload.
- [ ] Verify the API documentation and required endpoints.
- [ ] Check Git status before deployment.
---

# Final Demo Sequence

The following sequence can be used to demonstrate the working StudySync backend:

1. Start PostgreSQL and activate the virtual environment.
2. Start the FastAPI server.
3. Open `/health` and verify PostgreSQL connectivity.
4. Open `/docs` to access Swagger UI.
5. Create a new user using `POST /users`.
6. Log in using `POST /auth/login` and obtain a JWT access token.
7. Authorize Swagger using the Bearer token.
8. Access the authenticated user's protected resource using `GET /users/{user_id}`.
9. Verify resource ownership by attempting to access another user's resource and confirming the `403 Forbidden` response.
10. Test `GET /study-tip` and verify the response from the external Study Tip service.
11. Run the complete automated test suite using `python -m pytest`.
12. Verify that Git is clean and the latest changes are pushed to GitHub.

### Core Working Flow

Health Check -> User Registration -> Login -> JWT Authentication -> Protected Resource -> Authorization -> Study Tip Service -> Automated Tests
