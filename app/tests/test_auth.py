def test_register_and_login(client):
    # register
    resp = client.post("/auth/register", json={"email": "newuser@example.com", "password": "pw"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "newuser@example.com"

    # login
    r2 = client.post("/auth/token", data={"username": "newuser@example.com", "password": "pw"})
    assert r2.status_code == 200
    assert "access_token" in r2.json()
