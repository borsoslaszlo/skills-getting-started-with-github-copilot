"""
Backend FastAPI tests using the AAA (Arrange-Act-Assert) pattern.
Run with: pytest
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (no setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure clean state
    client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Act: Sign up
    response_signup = client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Assert
    assert response_signup.status_code == 200
    assert f"Signed up {test_email}" in response_signup.json()["message"]

    # Act: Duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Assert
    assert response_dup.status_code == 400

    # Act: Unregister
    response_del = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Assert
    assert response_del.status_code == 200
    assert f"Removed {test_email}" in response_del.json()["message"]

    # Act: Unregister again (should fail)
    response_del2 = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Assert
    assert response_del2.status_code == 404
