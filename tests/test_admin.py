from fastapi.testclient import TestClient


def test_set_maintenance_mode(client: TestClient, admin_token_headers, test_parking_slot):
    response = client.post(
        "/api/admin/maintenance",
        headers=admin_token_headers,
        json={
            "slot_ids": [test_parking_slot.id],
            "enable": True
        }
    )
    assert response.status_code == 200
    
    # Verify the slot is in maintenance mode
    response = client.get(f"/api/parking-slots/{test_parking_slot.id}", headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "maintenance"


def test_set_maintenance_mode_user(client: TestClient, user_token_headers, test_parking_slot):
    response = client.post(
        "/api/admin/maintenance",
        headers=user_token_headers,
        json={
            "slot_ids": [test_parking_slot.id],
            "enable": True
        }
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]