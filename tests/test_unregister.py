def test_unregister_success_removes_participant(client):
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown Activity/unregister", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_non_member_returns_400(client):
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": "notmember@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}