from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from adaptive_response.sessions import SessionCapacity, SessionExpired, SessionStore
from adaptive_response.web_app import create_app


def test_operator_sessions_are_isolated_and_stale_deploy_does_not_spend_twice():
    app = create_app()
    with TestClient(app) as first, TestClient(app) as second:
        before = first.get("/api/state").json()
        other = second.get("/api/state").json()
        top = before["global_recommendations"][0]
        action = {"site_id": top["site_id"], "effort": 6, "expected_round": 0}
        assert first.post("/api/deploy", json=action).status_code == 200
        assert second.get("/api/state").json() == other
        assert first.post("/api/deploy", json=action).status_code == 409
        assert first.get("/api/state").json()["resources"]["spent_budget"] == 6


def test_receipt_respects_truth_gate_then_exports_complete_evaluation():
    with TestClient(create_app()) as client:
        current = client.get("/api/state").json()
        response = client.get("/api/receipt")
        assert response.headers["content-disposition"].endswith('receipt.json"')
        receipt = response.json()
        assert receipt["mode"] == "simulation_evaluation"
        assert receipt["state"]["performance"] is None
        assert receipt["state"]["incident"]["truth_family"] is None
        assert all(node.get("true_occupied") is None for node in receipt["state"]["nodes"])
        assert client.post("/api/reveal").status_code == 409
        while not current["can_reveal"]:
            top = current["global_recommendations"][0]
            response = client.post("/api/deploy", json={"site_id": top["site_id"],
                "effort": top["recommended_effort"], "expected_round": current["resources"]["round"]})
            assert response.status_code == 200
            current = response.json()
        assert client.post("/api/reveal").status_code == 200
        final = client.get("/api/receipt").json()["state"]
        assert final["revealed"]
        assert final["performance"]["you"]["effort_spent"] == 18


@pytest.mark.parametrize("effort", [True, "1", 1.0, 0, 2, 7])
def test_api_rejects_invalid_or_coerced_effort(effort):
    with TestClient(create_app()) as client:
        assert client.post("/api/deploy", json={"site_id": "123", "effort": effort}).status_code == 422


def test_reset_contract_and_cross_origin_mutation():
    with TestClient(create_app()) as client:
        assert client.post("/api/reset", json={"case_id": "incident_079", "seed": 1}).status_code == 422
        assert client.post("/api/reset", json={"case_id": "incident_079", "extra": True}).status_code == 422
        assert client.post("/api/reset", json={"seed": -1}).status_code == 422
        assert client.post("/api/reset", json={}, headers={"Origin": "https://unrelated.example"}).status_code == 403
        assert client.post("/api/reveal").status_code == 409


def test_health_and_asset_readiness_do_not_allocate_a_session():
    def forbidden_factory():
        raise AssertionError("Health endpoints must not construct an incident.")
    with TestClient(create_app(SessionStore(factory=forbidden_factory))) as client:
        assert client.get("/healthz").json()["status"] == "ok"
        assert client.get("/readyz").json()["status"] == "ready"
        assert client.get("/static/crab.svg").status_code == 200


def test_store_is_bounded_and_expires_idle_sessions_without_silent_reset():
    now = [0.0]
    store = SessionStore(capacity=1, ttl=10, clock=lambda: now[0], factory=object)
    token, _ = store.run(None, lambda session: None, create=True)
    with pytest.raises(SessionCapacity):
        store.run(None, lambda session: None, create=True)
    now[0] = 10
    with pytest.raises(SessionExpired):
        store.run(token, lambda session: None)
    new_token, _ = store.run(None, lambda session: None, create=True)
    assert token != new_token


def test_active_request_cannot_expire_and_other_sessions_can_progress():
    now = [0.0]
    store = SessionStore(capacity=2, ttl=10, clock=lambda: now[0], factory=object)
    token, _ = store.run(None, lambda session: None, create=True)
    started, finish = Event(), Event()
    def slow_operation(session):
        started.set()
        assert finish.wait(5)
    with ThreadPoolExecutor(max_workers=2) as executor:
        running = executor.submit(store.run, token, slow_operation)
        assert started.wait(5)
        try:
            now[0] = 20
            second, _ = store.run(None, lambda session: None, create=True)
            with pytest.raises(SessionCapacity):
                store.run(None, lambda session: None, create=True)
            assert second != token
        finally:
            finish.set()
        running.result(timeout=5)
    assert store.run(token, lambda session: "retained")[1] == "retained"
