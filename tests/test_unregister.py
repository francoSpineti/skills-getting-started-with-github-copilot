"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint
"""
import pytest


def test_unregister_success(client):
    """Test successful unregister of a participant"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    # Initial check
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])
    
    # Unregister
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    new_count = len(response.json()["Chess Club"]["participants"])
    assert new_count == initial_count - 1
    assert "michael@mergington.edu" not in response.json()["Chess Club"]["participants"]


def test_unregister_nonexistent_activity(client):
    """Test unregister from an activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant_not_in_activity(client):
    """Test unregister of a participant not in the activity"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "not.registered@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Student not found" in response.json()["detail"]


def test_unregister_all_participants(client):
    """Test unregistering all participants from an activity"""
    # Get initial participants
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"].copy()
    
    # Unregister each one
    for participant in participants:
        client.delete(
            "/activities/Chess Club/unregister",
            params={"email": participant}
        )
    
    # Verify all are removed
    response = client.get("/activities")
    assert len(response.json()["Chess Club"]["participants"]) == 0


def test_unregister_and_signup_again(client):
    """Test that a participant can unregister and then sign up again"""
    email = "michael@mergington.edu"
    
    # Unregister
    response1 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Signup again
    response2 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify participant is back
    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]


def test_unregister_twice_fails(client):
    """Test that unregistering twice fails on the second attempt"""
    email = "michael@mergington.edu"
    
    # First unregister should succeed
    response1 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response2.status_code == 404


def test_unregister_with_empty_email(client):
    """Test unregister with empty email"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": ""}
    )
    # Empty email won't match any participant
    assert response.status_code == 404


def test_unregister_other_participants_unaffected(client):
    """Test that unregistering one participant doesn't affect others"""
    # Get initial state
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"].copy()
    
    # Unregister one
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify other participant is still there
    response = client.get("/activities")
    remaining_participants = response.json()["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in remaining_participants
    assert "michael@mergington.edu" not in remaining_participants
