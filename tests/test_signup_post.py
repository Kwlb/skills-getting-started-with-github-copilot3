from urllib.parse import quote

import src.app as app_module


def test_signup_adds_participant_successfully(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": new_email},
    )
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert body["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in app_module.activities[activity_name]["participants"]


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    missing_activity = "Unknown Club"
    email = "student@mergington.edu"
    encoded_activity_name = quote(missing_activity, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = app_module.activities[activity_name]["participants"][0]
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": existing_email},
    )
    body = response.json()

    # Assert
    assert response.status_code == 400
    assert body["detail"] == "Student already signed up for this activity"


def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    max_participants = app_module.activities[activity_name]["max_participants"]
    app_module.activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]
    email = "late.student@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )
    body = response.json()

    # Assert
    assert response.status_code == 400
    assert body["detail"] == "Activity is full"
    assert email not in app_module.activities[activity_name]["participants"]