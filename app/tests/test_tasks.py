import datetime

def test_create_update_delete_task(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    task = {
        "title": "Test Task",
        "description": "desc",
        "tag": "Exercise",
        "status": "Incomplete",
        "due_datetime": datetime.datetime.utcnow().isoformat()
    }
    r = client.post("/tasks/", json=task, headers=headers)
    assert r.status_code == 200
    tid = r.json()["id"]

    # update
    task["title"] = "Updated Task"
    r2 = client.put(f"/tasks/{tid}", json=task, headers=headers)
    assert r2.status_code == 200
    assert r2.json()["title"] == "Updated Task"

    # delete
    r3 = client.delete(f"/tasks/{tid}", headers=headers)
    assert r3.status_code == 200
    assert r3.json()["success"] is True
