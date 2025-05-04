from fastapi.testclient import TestClient


def test_read_users_admin(client: TestClient, admin_token_headers):
    response = client.get("/api/users/", headers=admin_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  


def test_read_users_regular_user(client: TestClient, user_token_headers):
    response = client.get("/api/users/", headers=user_token_headers)
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]


def test_read_user_me(client: TestClient, user_token_headers, test_user):
    response = client.get("/api/users/me", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["role"] == test_user.role


def test_update_user_me(client: TestClient, user_token_headers):
    response = client.put(
        "/api/users/me",
        headers=user_token_headers,
        json={"email": "updated@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"

def test_set_maintenance_mode_admin(client: TestClient, admin_token_headers, test_parking_slot):
    response = client.post(
        "/api/admin/maintenance",
        headers=admin_token_headers,
        json={
            "slot_ids": [test_parking_slot.id],
            "enable": True
        }
    )
    assert response.status_code == 200

