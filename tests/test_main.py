from fastapi.testclient import TestClient

from app.main import app
from app.store import STORE

client = TestClient(app)


def setup_function() -> None:
    STORE.reset()


def test_health() -> None:
    assert client.get("/health").json() == {"ok": True}


def test_add_score_accumulates() -> None:
    client.post("/scores", json={"name": "ana", "points": 10})
    r = client.post("/scores", json={"name": "ana", "points": 5})
    assert r.json() == {"name": "ana", "total": 15}


def test_leaderboard_sorted() -> None:
    client.post("/scores", json={"name": "ana", "points": 10})
    client.post("/scores", json={"name": "leo", "points": 30})
    top = client.get("/leaderboard").json()
    assert top[0] == {"name": "leo", "points": 30}


def test_reading_a_total_does_not_add_a_player() -> None:
    assert STORE.total("ghost") == 0
    assert client.get("/leaderboard").json() == []


def _post(name: str, points: int) -> None:
    client.post("/scores", json={"name": name, "points": points})


def test_stats_empty() -> None:
    r = client.get("/stats")
    assert r.status_code == 200
    assert r.json() == {"players": 0, "average": 0.0}
    assert isinstance(r.json()["average"], float)


def test_stats_one_player() -> None:
    _post("ana", 50)
    assert client.get("/stats").json() == {"players": 1, "average": 50.0}


def test_stats_several_players() -> None:
    _post("A", 10)
    _post("B", 20)
    _post("C", 30)
    assert client.get("/stats").json() == {"players": 3, "average": 20.0}


def test_stats_accumulates_same_name() -> None:
    _post("A", 10)
    _post("A", 5)
    _post("B", 5)
    assert client.get("/stats").json() == {"players": 2, "average": 10.0}


def test_stats_non_integer_average() -> None:
    _post("A", 1)
    _post("B", 2)
    assert client.get("/stats").json()["average"] == 1.5


def test_stats_does_not_create_entries() -> None:
    client.get("/stats")
    assert client.get("/leaderboard").json() == []
    assert client.get("/stats").json()["players"] == 0


def test_stats_counts_zero_point_player() -> None:
    _post("zero", 0)
    assert client.get("/stats").json() == {"players": 1, "average": 0.0}


def test_rejects_bad_input() -> None:
    assert client.post("/scores", json={"name": "", "points": 10}).status_code == 422
    assert client.get("/leaderboard?limit=0").status_code == 422
