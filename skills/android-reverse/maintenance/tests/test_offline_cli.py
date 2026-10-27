"""Offline CLI coverage with a synthetic, non-installation DEX fixture."""
import importlib.util
import json
import hashlib
from pathlib import Path
import struct
import zlib

import pytest

from conftest import ALLOWED, load_script, run_script


def make_dex(path, target=None):
    builder_path = Path(__file__).parent / "fixtures" / "make_fixture_dex.py"
    spec = importlib.util.spec_from_file_location("fixture_builder", builder_path)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    if target:
        builder.TARGET = target
    data, _, _, _ = builder.build()
    path.write_bytes(data)
    return path


@pytest.mark.parametrize("name", sorted(ALLOWED))
def test_help_is_local_and_completes(name):
    result = run_script(name, ["--help"])
    assert result.returncode == 0, result.output
    assert not result.has_traceback
    assert len(result.output) > 20


def test_dex_strings_finds_known_class(tmp_path):
    dex = make_dex(tmp_path / "sample.dex")
    result = run_script("dex_strings.py", [dex, "--find", "Target"])
    assert result.returncode == 0, result.output
    assert "Lcom/example/Target;" in result.stdout


def test_class_diff_identifies_known_added_and_removed_class(tmp_path):
    a = make_dex(tmp_path / "a.dex")
    b = make_dex(tmp_path / "b.dex", "Lcom/example/Second;")
    result = run_script("dex_classdiff.py", [a, b])
    assert result.returncode == 1
    assert "A-only: Lcom/example/Target;" in result.stdout
    assert "B-only: Lcom/example/Second;" in result.stdout


def test_find_instructions_matches_known_calls(tmp_path):
    dex = make_dex(tmp_path / "sample.dex")
    result = run_script("dex_find_insn.py", [dex, "--class", "Caller", "--method", "go"])
    assert result.returncode == 0, result.output
    assert "invoke-static" in result.stdout
    assert "Target" in result.stdout


def test_class_diff_reports_non_interface_flag_change(tmp_path):
    a = make_dex(tmp_path / "a.dex")
    data = bytearray(a.read_bytes())
    class_defs = struct.unpack_from("<I", data, 0x64)[0]
    flags = struct.unpack_from("<I", data, class_defs + 4)[0]
    struct.pack_into("<I", data, class_defs + 4, flags ^ 0x10)
    data[12:32] = hashlib.sha1(data[32:]).digest()
    struct.pack_into("<I", data, 8, zlib.adler32(data[12:]) & 0xffffffff)
    b = tmp_path / "b.dex"
    b.write_bytes(data)
    result = run_script("dex_classdiff.py", [a, b])
    assert result.returncode == 1
    assert "access_flags diff (same interface-ness): 1" in result.stdout


def test_dump_validation_reports_known_structure(tmp_path):
    dex = make_dex(tmp_path / "sample.dex")
    result = run_script("dex_dump_validate.py", [dex, "--json"])
    assert result.returncode == 0, result.output
    report = json.loads(result.stdout)
    profile = report["profiles"][0]
    assert profile["classes"] == 2
    assert profile["checksum_ok"] is True
    assert profile["signature_ok"] is True


def test_java2c_probe_does_not_promote_metrics_to_a_verdict(tmp_path):
    dex = make_dex(tmp_path / "sample.dex")
    result = run_script("java2c_probe.py", ["--dex", dex, "--json"])
    assert result.returncode == 0, result.output
    report = json.loads(result.stdout)
    assert report["classification"]["verdict"] == "unconfirmed"
    assert "candidate" in report["classification"]


def test_kotlin_build_requires_explicit_new_output(tmp_path):
    sources = tmp_path / "sources"
    sources.mkdir()
    result = run_script("kotlin_name_recovery.py", [sources])
    assert result.returncode == 2
    result = run_script("kotlin_name_recovery.py", [sources, "--out", sources])
    assert result.returncode == 2


def test_blob_round_trip_handles_binary_data():
    blob = load_script("blob_decode.py")
    payload = b"\x00\x01non-text\xff"
    assert blob.outer_decode(blob.outer_encode(payload, "base64"), "base64") == payload
