import json
import pytest


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_create_task_minimal(client):
    r = client.post("/api/tasks/", json={"title": "Buy milk"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["title"] == "Buy milk"
    assert data["status"] == "todo"
    assert data["priority"] == "medium"


def test_create_task_missing_title(client):
    r = client.post("/api/tasks/", json={"description": "no title"})
    assert r.status_code == 422
    assert "title" in r.get_json()["errors"]


def test_create_task_invalid_status(client):
    r = client.post("/api/tasks/", json={"title": "x", "status": "flying"})
    assert r.status_code == 422


def test_list_tasks_empty(client):
    r = client.get("/api/tasks/")
    assert r.status_code == 200
    body = r.get_json()
    assert body["items"] == []
    assert body["total"] == 0


def test_list_tasks_filter_status(client):
    client.post("/api/tasks/", json={"title": "A", "status": "todo"})
    client.post("/api/tasks/", json={"title": "B", "status": "done"})
    r = client.get("/api/tasks/?status=done")
    items = r.get_json()["items"]
    assert len(items) == 1
    assert items[0]["title"] == "B"


def test_get_task(client):
    created = client.post("/api/tasks/", json={"title": "Get me"}).get_json()
    r = client.get(f"/api/tasks/{created['id']}")
    assert r.status_code == 200
    assert r.get_json()["id"] == created["id"]


def test_get_task_not_found(client):
    r = client.get("/api/tasks/9999")
    assert r.status_code == 404


def test_update_task(client):
    created = client.post("/api/tasks/", json={"title": "Old title"}).get_json()
    r = client.patch(f"/api/tasks/{created['id']}", json={"title": "New title", "status": "done"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["title"] == "New title"
    assert data["status"] == "done"


def test_delete_task(client):
    created = client.post("/api/tasks/", json={"title": "Delete me"}).get_json()
    r = client.delete(f"/api/tasks/{created['id']}")
    assert r.status_code == 204
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404


def test_task_with_tag(client):
    tag = client.post("/api/tags/", json={"name": "urgent", "color": "#ff0000"}).get_json()
    task = client.post("/api/tasks/", json={"title": "Tagged", "tag_ids": [tag["id"]]}).get_json()
    assert len(task["tags"]) == 1
    assert task["tags"][0]["name"] == "urgent"


def test_task_invalid_tag_id(client):
    r = client.post("/api/tasks/", json={"title": "Bad tag", "tag_ids": [9999]})
    assert r.status_code == 422


def test_search_tasks(client):
    client.post("/api/tasks/", json={"title": "Fix login bug"})
    client.post("/api/tasks/", json={"title": "Write docs"})
    r = client.get("/api/tasks/?search=login")
    items = r.get_json()["items"]
    assert len(items) == 1
    assert "login" in items[0]["title"].lower()


def test_ai_priority_heuristic_urgent(client):
    """With no API key, heuristic should detect 'urgent' keyword."""
    r = client.post("/api/tasks/", json={
        "title": "URGENT: fix outage",
        "use_ai_priority": True,
    })
    assert r.status_code == 201
    data = r.get_json()
    assert data["priority"] in ("critical", "high")
    assert data["ai_priority_reason"] is not None


def test_pagination(client):
    for i in range(5):
        client.post("/api/tasks/", json={"title": f"Task {i}"})
    r = client.get("/api/tasks/?page=1&per_page=2")
    body = r.get_json()
    assert len(body["items"]) == 2
    assert body["total"] == 5
    assert body["pages"] == 3
