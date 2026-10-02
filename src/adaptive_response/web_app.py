from __future__ import annotations

import json
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator, model_validator

from .resources import verify_assets
from .sessions import SessionCapacity, SessionExpired, SessionStore

WEB_DIR = Path(__file__).with_name("web")
COOKIE_NAME = "gtc_evaluation"


class ResetRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    seed: StrictInt | None = Field(default=None, ge=0, le=999_999)
    case_id: str | None = Field(default=None, min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")

    @model_validator(mode="after")
    def one_selector(self):
        if self.seed is not None and self.case_id is not None:
            raise ValueError("Use either seed or case_id, not both.")
        return self


class DeployRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    site_id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    effort: StrictInt
    expected_round: StrictInt | None = Field(default=None, ge=0)

    @field_validator("effort")
    @classmethod
    def valid_effort(cls, value):
        if value not in (1, 3, 6):
            raise ValueError("Effort must be 1, 3 or 6.")
        return value


def create_app(store: SessionStore | None = None) -> FastAPI:
    store = store if store is not None else SessionStore()
    app = FastAPI(title="Grab the Crab — Evaluation API", version=version("grab-the-crab"))
    app.state.sessions = store
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

    @app.middleware("http")
    async def response_policy(request: Request, call_next):
        if request.method == "POST":
            origin = request.headers.get("origin")
            expected = (request.url.scheme, request.url.netloc)
            supplied = urlsplit(origin) if origin else None
            if (supplied and (supplied.scheme, supplied.netloc) != expected) or request.headers.get("sec-fetch-site") == "cross-site":
                return JSONResponse({"detail": "Cross-origin changes are not allowed."}, status_code=403)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' https://server.arcgisonline.com https://tile.openstreetmap.org; "
            "connect-src 'self'; frame-ancestors 'none'; form-action 'none'"
        )
        if request.url.path in ("/docs", "/redoc"):
            # FastAPI's optional schema viewers load their own CDN scripts and
            # inline bootstrap. The evaluation dashboard keeps the stricter
            # policy above; these documentation routes retain their defaults.
            del response.headers["Content-Security-Policy"]
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    def call(request: Request, response: Response, operation, *, create=False):
        try:
            token, result = store.run(request.cookies.get(COOKIE_NAME), operation, create=create)
        except SessionCapacity as exc:
            raise HTTPException(503, str(exc), headers={"Retry-After": "60"}) from exc
        except (SessionExpired, RuntimeError, ValueError) as exc:
            raise HTTPException(409, str(exc)) from exc
        response.set_cookie(COOKIE_NAME, token, max_age=int(store.ttl), path="/api",
                            httponly=True, secure=request.url.scheme == "https", samesite="strict")
        return result

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    @app.get("/healthz")
    def health() -> dict:
        return {"status": "ok", "version": app.version, "mode": "simulation_evaluation"}

    @app.get("/readyz")
    def ready() -> dict:
        try:
            verify_assets()
        except (OSError, ValueError, KeyError) as exc:
            raise HTTPException(503, "Evaluation assets are missing or differ from the frozen receipt.") from exc
        return {"status": "ready", "version": app.version}

    @app.get("/api/state")
    def state(request: Request, response: Response) -> dict:
        return call(request, response, lambda session: session.snapshot(), create=True)

    @app.get("/api/cases")
    def cases(request: Request, response: Response) -> dict:
        return call(request, response, lambda session: session.case_library(), create=True)

    @app.post("/api/reset")
    def reset(body: ResetRequest, request: Request, response: Response) -> dict:
        return call(request, response, lambda session: session.reset(seed=body.seed, case_id=body.case_id), create=True)

    @app.post("/api/deploy")
    def deploy(body: DeployRequest, request: Request, response: Response) -> dict:
        def operation(session):
            if body.expected_round is not None and session.snapshot()["resources"]["round"] != body.expected_round:
                raise ValueError("Incident changed since this decision. Reload the current state before deploying.")
            return session.deploy(site_id=body.site_id, effort=body.effort)
        return call(request, response, operation)

    # Retain the original rehearsal endpoints for existing integrations.
    @app.post("/api/plan")
    def plan(request: Request, response: Response) -> dict:
        return call(request, response, lambda session: session.plan())

    @app.post("/api/execute")
    def execute(request: Request, response: Response) -> dict:
        return call(request, response, lambda session: session.execute())

    @app.post("/api/reveal")
    def reveal(request: Request, response: Response) -> dict:
        return call(request, response, lambda session: session.reveal())

    @app.get("/api/receipt")
    def receipt(request: Request) -> Response:
        response = Response(media_type="application/json")
        snap = call(request, response, lambda session: session.snapshot())
        response.headers["Content-Disposition"] = f'attachment; filename="grab-the-crab-{snap["case"]["case_id"]}-receipt.json"'
        response.body = json.dumps({"schema_version": 1, "software_version": app.version,
                                    "mode": "simulation_evaluation", "state": snap}, indent=2, allow_nan=False).encode()
        response.headers["Content-Length"] = str(len(response.body))
        return response

    return app


app = create_app()


def main() -> None:
    import uvicorn
    uvicorn.run("adaptive_response.web_app:app", host="127.0.0.1", port=8000, reload=False, workers=1)


if __name__ == "__main__":
    main()
