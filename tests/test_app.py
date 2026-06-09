from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Soccer Team"]["participants"] = []


def test_signup_adds_participant_and_returns_success():
    reset_activities()
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    activities[activity_name]["participants"] = ["michael@mergington.edu"]

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email.lower()} for {activity_name}"}
    assert email.lower() in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant():
    reset_activities()
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_rejects_invalid_email():
    reset_activities()
    response = client.post("/activities/Soccer Team/signup?email=not-an-email")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email address"


def test_unregister_removes_participant_successfully():
    reset_activities()
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email.lower()} from {activity_name}"}
    assert email.lower() not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity():
    reset_activities()
    response = client.delete("/activities/Does Not Exist/unregister?email=test@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_if_student_not_signed_up():
    reset_activities()
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
