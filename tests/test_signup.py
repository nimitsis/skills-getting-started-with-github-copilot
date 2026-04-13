"""Tests for activity signup endpoint."""
import pytest


def test_signup_success(client):
    """Test successful signup for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    payload = {"email": email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully signed up"}
    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_duplicate(client):
    """Test signup with already registered email."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    payload = {"email": email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Already signed up"}


def test_signup_invalid_activity(client):
    """Test signup for non-existing activity."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"
    payload = {"email": email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_missing_email(client):
    """Test signup without email in payload."""
    # Arrange
    activity_name = "Chess Club"
    payload = {}  # Missing email

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Email is required"}


def test_signup_multiple_participants(client):
    """Test multiple signups accumulate in participants list."""
    # Arrange
    activity_name = "Art Studio"  # initial participants: 1
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

    # Act
    for email in emails:
        payload = {"email": email}
        response = client.post(f"/activities/{activity_name}/signup", json=payload)
        assert response.status_code == 200

    # Assert
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert len(participants) == 4  # initial 1 + 3 new
    for email in emails:
        assert email in participants