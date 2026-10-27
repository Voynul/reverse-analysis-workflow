#!/usr/bin/env python3
"""Run the optional offline suite without loading unrelated global pytest plugins."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    if importlib.util.find_spec("pytest") is None:
        print("pytest is not available in this interpreter; tests were not run.", file=sys.stderr)
        print("Use an isolated test environment with pytest, then run this file again.", file=sys.stderr)
        sys.exit(2)
    environment = dict(os.environ)
    environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-c", str(ROOT / "maintenance" / "pytest.ini"),
         "-q", "-p", "no:cacheprovider", *sys.argv[1:]],
        cwd=ROOT, env=environment,
    )
    sys.exit(result.returncode)
