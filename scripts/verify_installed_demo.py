"""Run with the wheel environment's Python from outside the checkout."""
import json
import sys
from pathlib import Path

import adaptive_response
from fastapi.testclient import TestClient
from adaptive_response.web_app import create_app
from adaptive_response.resources import verify_assets

if __name__ == "__main__":
    checkout = Path(__file__).resolve().parents[1]
    assert not Path(adaptive_response.__file__).resolve().is_relative_to(checkout / "src"), "Use an installed wheel, not the editable checkout."
    verify_assets()
    with TestClient(create_app()) as client:
        for path in ("/", "/static/app.js", "/static/styles.css", "/static/crab.svg", "/healthz", "/readyz"):
            assert client.get(path).status_code == 200, path
        snap = client.get("/api/state").json()
        assert snap["case"]["count"] == 100
        assert client.post("/api/reveal").status_code == 409
        while not snap["can_reveal"]:
            top = snap["global_recommendations"][0]
            response = client.post("/api/deploy", json={"site_id": top["site_id"],
                "effort": top["recommended_effort"], "expected_round": snap["resources"]["round"]})
            assert response.status_code == 200, response.text
            snap = response.json()
        assert client.post("/api/reveal").status_code == 200
        receipt = client.get("/api/receipt").json()
        assert receipt["state"]["resources"]["spent_budget"] == 18
        assert "torch" not in sys.modules
        print(json.dumps({"installed_wheel": "ok", "software_version": receipt["software_version"],
                          "case": snap["case"]["case_id"], "missions": snap["resources"]["round"],
                          "effort_spent": 18, "torch_imported": False}))
