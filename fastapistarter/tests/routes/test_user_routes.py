from httpx import AsyncClient

# No explicit 'import pytest' needed here.
# The runner automatically discovers functions starting with 'test_'.

# Testdata
USER_DATA = {"username": "api_user", "password": "secret_password"}


async def test_create_user_endpoint(client: AsyncClient):
    response = await client.post("/users/", json=USER_DATA)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == USER_DATA["username"]
    assert "id" in data
    # Testing Schema Response Model
    assert "password" not in data


async def test_create_duplicate_user_fails(client: AsyncClient):
    await client.post("/users/", json=USER_DATA)

    response = await client.post("/users/", json=USER_DATA)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


async def test_read_user_endpoint(client: AsyncClient):
    # Setup
    create_res = await client.post("/users/", json=USER_DATA)
    user_id = create_res.json()["id"]

    # Test
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == USER_DATA["username"]


async def test_read_user_not_found(client: AsyncClient):
    response = await client.get("/users/999999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


async def test_update_user_endpoint(client: AsyncClient):
    # Setup
    create_res = await client.post("/users/", json=USER_DATA)
    user_id = create_res.json()["id"]

    # Update Payload (only Username)
    response = await client.patch(
        f"/users/{user_id}", json={"username": "updated_api_user"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == "updated_api_user"


async def test_delete_user_endpoint(client: AsyncClient):
    # Setup
    create_res = await client.post("/users/", json=USER_DATA)
    user_id = create_res.json()["id"]

    # Delete
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204  # No Content

    # Verify: assert 404
    check_response = await client.get(f"/users/{user_id}")
    assert check_response.status_code == 404
