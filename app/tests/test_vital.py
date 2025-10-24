import datetime

def test_post_and_get_vitals(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "hydration": 55.0,
        "sleep": 7.5,
        "heartbeat": 72,
        "bp_systolic": 120,
        "bp_diastolic": 80,
        "steps": 5000,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    r = client.post("/vitals/", json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["hydration"] == 55.0

    r2 = client.get("/vitals/", headers=headers)
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)
    assert len(r2.json()) >= 1
