"""
Tests for the GET /activities endpoint
"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert len(activities) == 3
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_has_correct_structure(client):
    """Test that activity objects have the correct structure"""
    response = client.get("/activities")
    activities = response.json()
    
    activity = activities["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_get_activities_includes_participants(client):
    """Test that participants are included in activities"""
    response = client.get("/activities")
    activities = response.json()
    
    chess_participants = activities["Chess Club"]["participants"]
    assert len(chess_participants) == 2
    assert "michael@mergington.edu" in chess_participants
    assert "daniel@mergington.edu" in chess_participants


def test_get_activities_includes_max_participants(client):
    """Test that max_participants is included"""
    response = client.get("/activities")
    activities = response.json()
    
    assert activities["Chess Club"]["max_participants"] == 12
    assert activities["Programming Class"]["max_participants"] == 20
    assert activities["Gym Class"]["max_participants"] == 30
