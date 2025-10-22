def test_ml_analyze(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/ml/analyze", json={"symptom_input": "headache and fever"}, headers=headers)
    assert r.status_code == 200
    assert "prediction" in r.json()
