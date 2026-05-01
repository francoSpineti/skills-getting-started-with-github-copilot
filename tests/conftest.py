"""
Pytest configuration and fixtures for FastAPI tests
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture
def mock_activities():
    """Provide mock activity data"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }


@pytest.fixture(autouse=True)
def reset_activities(mock_activities):
    """Reset activities to mock data before each test"""
    # Clear the current activities
    activities.clear()
    # Repopulate with mock data
    activities.update(mock_activities)
    yield
    # Cleanup after test
    activities.clear()
