def test_contacts_crud(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    c = {"name": "Bob", "relationship": "Friend", "phone": "123", "email": "bob@example.com", "favourite": True}
    r = client.post("/contacts/", json=c, headers=headers)
    assert r.status_code == 200
    cid = r.json()["id"]

    r2 = client.get("/contacts/", headers=headers)
    assert r2.status_code == 200
    assert any(x["id"] == cid for x in r2.json())

    # update
    c["name"] = "Bobby"
    r3 = client.put(f"/contacts/{cid}", json=c, headers=headers)
    assert r3.status_code == 200
    assert r3.json()["name"] == "Bobby"

    # delete
    r4 = client.delete(f"/contacts/{cid}", headers=headers)
    assert r4.status_code == 200
    assert r4.json()["success"] is True
