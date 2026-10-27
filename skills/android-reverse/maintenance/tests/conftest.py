"""Offline-only test adapter; never opens a device or imports device scripts."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import pytest

SKILL_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = SKILL_ROOT / "scripts" / "offline"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
ALLOWED = {
    "apk_diff.py", "blob_decode.py", "dex_classdiff.py", "dex_dump_validate.py",
    "dex_find_insn.py", "dex_strings.py", "dexutil.py", "java2c_probe.py",
    "js_obf_detect.py", "jsvmp_loader_decode.py", "kotlin_name_recovery.py",
    "protobuf_decode_raw.py", "trace_addr2sym.py", "trace_diff.py",
    "vm_handler_slice.py",
}
for directory in (SCRIPTS_DIR, Path(__file__).resolve().parent):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))
_loaded = {}


def script_path(name):
    if name not in ALLOWED:
        raise ValueError("not an approved offline test script: " + name)
    return SCRIPTS_DIR / name


def load_script(name):
    if name not in _loaded:
        path = script_path(name)
        module_name = "android_reverse_offline_" + path.stem
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(name)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        _loaded[name] = module
    return _loaded[name]


class ScriptResult:
    def __init__(self, argv, returncode, stdout, stderr, timed_out=False):
        self.argv = argv
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.timed_out = timed_out

    @property
    def output(self):
        return self.stdout + self.stderr

    @property
    def has_traceback(self):
        return "Traceback (most recent call last)" in self.output


def run_script(name, args=(), timeout=60, cwd=None, stdin=None, env=None):
    argv = [sys.executable, str(script_path(name)), *(str(a) for a in args)]
    child_env = dict(os.environ)
    child_env.update(PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    if env:
        child_env.update(env)
    with tempfile.TemporaryDirectory(prefix="android-reverse-test-") as temporary:
        try:
            result = subprocess.run(
                argv, capture_output=True, text=True, encoding="utf-8",
                errors="replace", input=stdin, timeout=timeout,
                cwd=str(cwd or temporary), env=child_env,
            )
            return ScriptResult(argv, result.returncode, result.stdout, result.stderr)
        except subprocess.TimeoutExpired as exc:
            def text(value):
                return value.decode("utf-8", "replace") if isinstance(value, bytes) else value or ""
            return ScriptResult(argv, None, text(exc.stdout), text(exc.stderr), True)


def require_path(path, why):
    if not Path(path).exists():
        pytest.skip("fixture absent: %s (%s)" % (path, why))
    return Path(path)


@pytest.fixture(scope="session")
def scripts_dir():
    return SCRIPTS_DIR


@pytest.fixture(scope="session")
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture(scope="session")
def bench_l1l3():
    pytest.skip("upstream private benchmark is not shipped; no target result is inferred")
