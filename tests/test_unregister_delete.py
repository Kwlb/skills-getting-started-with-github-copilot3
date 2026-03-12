from urllib.parse import quote

import src.app as app_module


def test_unregister_removes_participant_successfully(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = app_module.activities[activity_name]["participants"][0]
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": participant_email},
    )
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert body["message"] == f"Unregistered {participant_email} from {activity_name}"
    assert participant_email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    missing_activity = "Unknown Club"
    email = "student@mergington.edu"
    encoded_activity_name = quote(missing_activity, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_unregister_returns_not_found_for_non_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Student is not signed up for this activity"