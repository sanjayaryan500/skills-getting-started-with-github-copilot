from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity():
    response = client.delete("/activities/Does Not Exist/unregister?email=test@example.com")
    assert response.status_code == 404
