"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""
import pytest


def test_signup_success(client):
    """Test successful signup of a new participant"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "new.student@mergington.edu"}
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds the participant"""
    # Initial check
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])
    
    # Signup
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "new.student@mergington.edu"}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    new_count = len(response.json()["Chess Club"]["participants"])
    assert new_count == initial_count + 1
    assert "new.student@mergington.edu" in response.json()["Chess Club"]["participants"]


def test_signup_nonexistent_activity(client):
    """Test signup to an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "new.student@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_participant(client):
    """Test that duplicate signup is prevented"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_duplicate_does_not_add_participant(client):
    """Test that duplicate signup doesn't add the participant again"""
    # Try to signup existing participant
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify participant count didn't increase
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert participants.count("michael@mergington.edu") == 1


def test_signup_with_empty_email(client):
    """Test signup with empty email"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": ""}
    )
    # Empty email should still be accepted and added by the API
    # (validation could be improved, but testing current behavior)
    assert response.status_code == 200


def test_signup_multiple_different_students(client):
    """Test that multiple different students can sign up"""
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "student1@mergington.edu"}
    )
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "student2@mergington.edu"}
    )
    
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert "student1@mergington.edu" in participants
    assert "student2@mergington.edu" in participants
    assert len(participants) == 4  # 2 original + 2 new


def test_signup_to_different_activities(client):
    """Test that same student can signup to multiple activities"""
    email = "new.student@mergington.edu"
    
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify in both activities
    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]
    assert email in response.json()["Programming Class"]["participants"]
