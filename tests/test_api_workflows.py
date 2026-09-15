import pytest


@pytest.mark.asyncio
async def test_main_user_workflow(client):
    # 1. Create a new user
    create_response = await client.post(
        "/users",
        json={
            "name": "Workflow User",
            "email": "workflow@example.com",
            "password": "Password123!"
        }
    )

    assert create_response.status_code == 201

    created_user = create_response.json()

    assert created_user["name"] == "Workflow User"
    assert created_user["email"] == "workflow@example.com"
    assert "password" not in created_user
    assert "password_hash" not in created_user

    user_id = created_user["id"]

    # 2. Login with the created user
    login_response = await client.post(
        "/auth/login",
        json={
            "email": "workflow@example.com",
            "password": "Password123!"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    access_token = login_data["access_token"]

    # 3. Access the authenticated user's profile
    user_response = await client.get(
        f"/users/{user_id}",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert user_response.status_code == 200

    user_data = user_response.json()

    assert user_data["id"] == user_id
    assert user_data["name"] == "Workflow User"
    assert user_data["email"] == "workflow@example.com"


@pytest.mark.asyncio
async def test_user_creation_validation_failure(client):
    # Password is intentionally missing.
    response = await client.post(
        "/users",
        json={
            "name": "Invalid User",
            "email": "invalid@example.com"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["status_code"] == 422
    assert data["error"]["message"] == "Invalid request data"
    assert "details" in data["error"]


@pytest.mark.asyncio
async def test_user_cannot_access_another_users_resource(client):
    # Create first user
    first_user_response = await client.post(
        "/users",
        json={
            "name": "First User",
            "email": "first@example.com",
            "password": "Password123!"
        }
    )

    assert first_user_response.status_code == 201

    first_user = first_user_response.json()

    # Create second user
    second_user_response = await client.post(
        "/users",
        json={
            "name": "Second User",
            "email": "second@example.com",
            "password": "Password123!"
        }
    )

    assert second_user_response.status_code == 201

    second_user = second_user_response.json()

    # Login as the first user
    login_response = await client.post(
        "/auth/login",
        json={
            "email": "first@example.com",
            "password": "Password123!"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # First user tries to access second user's resource
    response = await client.get(
        f"/users/{second_user['id']}",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["error"]["status_code"] == 403
    assert data["error"]["message"] == (
        "You are not authorized to access this user's resource"
    )