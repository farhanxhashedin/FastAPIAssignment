from fastapi.testclient import TestClient


def test_create_feedback(client: TestClient, user_token_headers, test_parking_slot):
    response = client.post(
        "/api/feedback/",
        headers=user_token_headers,
        json={
            "rating": 5,
            "comment": "Great parking spot!",
            "parking_slot_id": test_parking_slot.id
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Great parking spot!"
    assert data["parking_slot_id"] == test_parking_slot.id


def test_read_feedback(client: TestClient, user_token_headers):
    # First create a feedback
    response = client.post(
        "/api/feedback/",
        headers=user_token_headers,
        json={
            "rating": 4,
            "comment": "Good experience"
        }
    )
    assert response.status_code == 201
    
    # Then read all feedback
    response = client.get("/api/feedback/", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["rating"] in [4, 5]  # From this test or the previous one