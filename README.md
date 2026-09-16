# StudySync - AI-Powered Student Study & Performance Platform

StudySync is a FastAPI-based backend platform designed to help students manage their study activities and academic performance.

The backend currently provides user management, JWT authentication, task search and filtering, study-tip service integration, structured error handling, and automated testing.

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