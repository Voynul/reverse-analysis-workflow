"""Known ZIP pairs test content, compression-only and duplicate-entry cases."""
import warnings
import zipfile

import pytest

from conftest import load_script, run_script

diff = load_script("apk_diff.py")


def archive(path, data, compression):
    with zipfile.ZipFile(path, "w", compression=compression) as stream:
        stream.writestr("assets/test.bin", data)


def test_equal_length_content_change(tmp_path):
    a, b = tmp_path / "a.apk", tmp_path / "b.apk"
    archive(a, b"abcd", zipfile.ZIP_STORED)
    archive(b, b"abce", zipfile.ZIP_STORED)
    result = run_script("apk_diff.py", [a, b])
    assert result.returncode == 0
    assert "content/compression changed: 1" in result.stdout
    assert "(SAME SIZE)" in result.stdout


def test_compression_only_change_is_reported(tmp_path):
    a, b = tmp_path / "a.apk", tmp_path / "b.apk"
    archive(a, b"same bytes" * 20, zipfile.ZIP_STORED)
    archive(b, b"same bytes" * 20, zipfile.ZIP_DEFLATED)
    assert diff.snapshot(a)["assets/test.bin"][1] == diff.snapshot(b)["assets/test.bin"][1]
    result = run_script("apk_diff.py", [a, b])
    assert "content/compression changed: 1" in result.stdout
    assert "ctype 0->8" in result.stdout


def test_duplicate_entries_are_refused(tmp_path):
    path = tmp_path / "duplicate.apk"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(path, "w") as stream:
            stream.writestr("assets/test.bin", b"first")
            stream.writestr("assets/test.bin", b"second")
    with pytest.raises(ValueError, match="duplicate ZIP entry"):
        diff.snapshot(path)


def test_identical_archives_are_identical(tmp_path):
    a, b = tmp_path / "a.apk", tmp_path / "b.apk"
    archive(a, b"same", zipfile.ZIP_STORED)
    archive(b, b"same", zipfile.ZIP_STORED)
    result = run_script("apk_diff.py", [a, b])
    assert "no differences at all" in result.stdout
