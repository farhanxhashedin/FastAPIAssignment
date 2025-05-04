import pytest
from fastapi.testclient import TestClient
from app.models.booking import Booking


@pytest.fixture
def test_booking(db, test_user, test_parking_slot):
    booking = Booking(
        user_id=test_user.id,
        parking_slot_id=test_parking_slot.id,
        status="active"
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def test_create_booking(client: TestClient, user_token_headers, test_parking_slot):
    response = client.post(
        "/api/bookings/",
        headers=user_token_headers,
        json={
            "parking_slot_id": test_parking_slot.id
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["parking_slot_id"] == test_parking_slot.id
    assert data["status"] == "active"


def test_create_booking_admin(client: TestClient, admin_token_headers, test_parking_slot):
    response = client.post(
        "/api/bookings/",
        headers=admin_token_headers,
        json={
            "parking_slot_id": test_parking_slot.id
        }
    )
    assert response.status_code == 403
    assert "Admins cannot make bookings" in response.json()["detail"]


def test_read_bookings(client: TestClient, user_token_headers, test_booking):
    response = client.get("/api/bookings/", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["id"] == test_booking.id


def test_read_booking(client: TestClient, user_token_headers, test_booking):
    response = client.get(f"/api/bookings/{test_booking.id}", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_booking.id
    assert data["status"] == "active"


def test_cancel_booking(client: TestClient, user_token_headers, test_booking):
    response = client.post(
        f"/api/bookings/{test_booking.id}/cancel",
        headers=user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_booking.id
    assert data["status"] == "cancelled"