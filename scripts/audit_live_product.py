"""Compatibility entry point: prefer `grab-the-crab audit --out ...`."""
from adaptive_response.cli import main
import sys

if __name__ == "__main__":
    sys.argv.insert(1, "audit")
    main()
