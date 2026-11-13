import pytest

from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def _create(client, title="Estudar DevOps", **extra):
    return client.post("/tasks", json={"title": title, **extra})


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_create_task(client):
    resp = _create(client, description="CI e IaC")
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] == 1
    assert body["title"] == "Estudar DevOps"
    assert body["done"] is False


def test_create_task_without_title(client):
    assert client.post("/tasks", json={}).status_code == 400
    assert client.post("/tasks", json={"title": "   "}).status_code == 400


def test_list_and_filter(client):
    _create(client, "A")
    _create(client, "B")
    client.post("/tasks/1/complete")
    assert len(client.get("/tasks").get_json()) == 2
    done = client.get("/tasks?done=true").get_json()
    pending = client.get("/tasks?done=false").get_json()
    assert [t["title"] for t in done] == ["A"]
    assert [t["title"] for t in pending] == ["B"]


def test_get_task(client):
    _create(client)
    assert client.get("/tasks/1").status_code == 200
    assert client.get("/tasks/99").status_code == 404


def test_update_task(client):
    _create(client)
    resp = client.put("/tasks/1", json={"title": "Novo", "description": "d", "done": True})
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["title"] == "Novo" and body["done"] is True
    assert client.put("/tasks/1", json={"title": ""}).status_code == 400
    assert client.put("/tasks/99", json={"title": "x"}).status_code == 404


def test_complete_task(client):
    _create(client)
    assert client.post("/tasks/1/complete").get_json()["done"] is True
    assert client.post("/tasks/99/complete").status_code == 404


def test_delete_task(client):
    _create(client)
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks/1").status_code == 404
    assert client.delete("/tasks/1").status_code == 404
