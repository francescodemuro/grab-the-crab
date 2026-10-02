from __future__ import annotations

import argparse
import json
from importlib.metadata import version
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Grab the Crab — reproducible buyer evaluation")
    parser.add_argument("--version", action="version", version=version("grab-the-crab"))
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Start the local evaluation UI (requires the ui extra)")
    demo.add_argument("--port", type=int, default=8000)
    audit = commands.add_parser("audit", help="Re-run the live policy against the paired static comparator")
    audit.add_argument("--out", type=Path, default=Path("artifacts/live-audit"))
    audit.add_argument("--case-id", action="append", help="Optional subset; omit to audit all 100 frozen cases")
    commands.add_parser("doctor", help="Verify bundled assets without network access or optional extras")
    args = parser.parse_args()
    if args.command == "demo":
        if not 1 <= args.port <= 65535:
            parser.error("Port must be between 1 and 65535.")
        try:
            import uvicorn
            from .web_app import app
        except ModuleNotFoundError as exc:
            parser.error(f"Install the UI extra first: pip install 'grab-the-crab[ui]'. Missing {exc.name}.")
        uvicorn.run(app, host="127.0.0.1", port=args.port, workers=1)
    elif args.command == "doctor":
        from .resources import verify_assets
        print(json.dumps({"status": "ok", "version": version("grab-the-crab"), "assets": verify_assets()}, indent=2))
    else:
        from .live_audit import run_live_audit, write_audit
        rows, summary = run_live_audit(args.case_id)
        write_audit(args.out, rows, summary)
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
