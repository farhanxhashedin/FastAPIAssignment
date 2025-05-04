from fastapi.testclient import TestClient


def test_create_parking_slot(client: TestClient, admin_token_headers):
    response = client.post(
        "/api/parking-slots/",
        headers=admin_token_headers,
        json={
            "slot_identifier": "B1",
            "status": "free",
            "label": "Test Slot B1",
            "floor": 1
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["slot_identifier"] == "B1"
    assert data["status"] == "free"
    assert data["label"] == "Test Slot B1"


def test_create_parking_slot_user(client: TestClient, user_token_headers):
    response = client.post(
        "/api/parking-slots/",
        headers=user_token_headers,
        json={
            "slot_identifier": "C1",
            "status": "free",
            "label": "Test Slot C1"
        }
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]


def test_read_parking_slots(client: TestClient, user_token_headers, test_parking_slot):
    response = client.get("/api/parking-slots/", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(slot["slot_identifier"] == test_parking_slot.slot_identifier for slot in data)


def test_read_parking_slot(client: TestClient, user_token_headers, test_parking_slot):
    response = client.get(f"/api/parking-slots/{test_parking_slot.id}", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["slot_identifier"] == test_parking_slot.slot_identifier
    assert data["status"] == test_parking_slot.status


def test_update_parking_slot(client: TestClient, admin_token_headers, test_parking_slot):
    response = client.put(
        f"/api/parking-slots/{test_parking_slot.id}",
        headers=admin_token_headers,
        json={
            "status": "maintenance",
            "label": "Updated Label"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "maintenance"
    assert data["label"] == "Updated Label"


def test_update_parking_slot_user(client: TestClient, user_token_headers, test_parking_slot):
    response = client.put(
        f"/api/parking-slots/{test_parking_slot.id}",
        headers=user_token_headers,
        json={
            "status": "maintenance"
        }
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]


def test_delete_parking_slot(client: TestClient, admin_token_headers, test_parking_slot):
    response = client.delete(
        f"/api/parking-slots/{test_parking_slot.id}",
        headers=admin_token_headers
    )
    assert response.status_code == 204


def test_bulk_create_parking_slots(client: TestClient, admin_token_headers):
    response = client.post(
        "/api/parking-slots/bulk",
        headers=admin_token_headers,
        json={
            "slots": [
                {"slot_identifier": "D1", "status": "free", "label": "Test D1", "floor": 2},
                {"slot_identifier": "D2", "status": "free", "label": "Test D2", "floor": 2}
            ]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data) == 2
    assert data[0]["slot_identifier"] == "D1"
    assert data[1]["slot_identifier"] == "D2"