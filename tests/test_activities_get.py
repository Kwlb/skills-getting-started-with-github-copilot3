REQUIRED_ACTIVITY_FIELDS = {"description", "schedule", "max_participants", "participants"}


def test_get_activities_returns_expected_structure(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert expected_activity_name in payload
    assert len(payload) == 9

    for activity_details in payload.values():
        assert REQUIRED_ACTIVITY_FIELDS.issubset(activity_details.keys())
        assert isinstance(activity_details["participants"], list)


def test_get_activities_disables_caching(client):
    # Arrange
    expected_cache_control = "no-store"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.headers.get("cache-control") == expected_cache_control