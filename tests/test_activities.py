from src import app as app_module


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_names = set(app_module.create_initial_activities().keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == expected_names


def test_get_activities_returns_expected_activity_shape(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activity = response.json()[activity_name]
    assert activity["description"] == "Learn strategies and compete in chess tournaments"
    assert activity["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert activity["max_participants"] == 12
    assert activity["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]