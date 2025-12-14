from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_sign_and_list_entries():
    # Clean up entries list (assuming in-memory global list)
    global_entries = app.extra.get("entries", [])
    global_entries.clear()

    # Step 1: Post a guest entry
    response = client.post("/sign", json={"name": "Alice", "message": "Hello World!"})
    assert response.status_code == 200
    assert response.json()["message"] == "Entry added successfully"

    # Step 2: Retrieve all entries
    response = client.get("/entries")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Alice"
    assert data[0]["message"] == "Hello World!"