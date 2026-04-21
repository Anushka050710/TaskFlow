def test_create_tag(client):
    r = client.post("/api/tags/", json={"name": "backend", "color": "#3b82f6"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["name"] == "backend"
    assert data["color"] == "#3b82f6"


def test_create_tag_duplicate(client):
    client.post("/api/tags/", json={"name": "dup"})
    r = client.post("/api/tags/", json={"name": "dup"})
    assert r.status_code == 409


def test_create_tag_invalid_color(client):
    r = client.post("/api/tags/", json={"name": "bad", "color": "red"})
    assert r.status_code == 422


def test_list_tags(client):
    client.post("/api/tags/", json={"name": "alpha"})
    client.post("/api/tags/", json={"name": "beta"})
    r = client.get("/api/tags/")
    assert r.status_code == 200
    names = [t["name"] for t in r.get_json()]
    assert "alpha" in names and "beta" in names


def test_delete_tag(client):
    tag = client.post("/api/tags/", json={"name": "gone"}).get_json()
    r = client.delete(f"/api/tags/{tag['id']}")
    assert r.status_code == 204


def test_delete_tag_not_found(client):
    r = client.delete("/api/tags/9999")
    assert r.status_code == 404
