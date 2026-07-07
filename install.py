#!/usr/bin/env python3
"""
Install the organized reverse-analysis skills, agents, and prompts.

The script checks the current user's home directory for:

- ~/.claude
- ~/.codex
- ~/.config/opencode

If a tool directory exists, the script copies the matching skills, agents, and
prompts into that tool's config tree. Existing different files are backed up
before being overwritten.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")


def copy_file(src: Path, dst: Path, dry_run: bool) -> None:
    if not src.is_file():
        print(f"SKIP missing file: {src}")
        return

    if dst.exists() and filecmp.cmp(src, dst, shallow=False):
        print(f"OK unchanged: {dst}")
        return

    if dst.exists():
        backup = dst.with_name(f"{dst.name}.bak-{STAMP}")
        print(f"BACKUP {dst} -> {backup}")
        if not dry_run:
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, backup)

    print(f"COPY {src} -> {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def copy_tree_contents(src_dir: Path, dst_dir: Path, dry_run: bool) -> None:
    if not src_dir.is_dir():
        print(f"SKIP missing dir: {src_dir}")
        return

    for src in src_dir.rglob("*"):
        if src.is_file():
            rel = src.relative_to(src_dir)
            copy_file(src, dst_dir / rel, dry_run)


def copy_named_dirs(src_parent: Path, dst_parent: Path, names: list[str], dry_run: bool) -> None:
    for name in names:
        copy_tree_contents(src_parent / name, dst_parent / name, dry_run)


def install_prompts(dst_root: Path, dry_run: bool) -> None:
    prompt_dst = dst_root / "prompts" / "reverse-analysis-workflow"
    copy_tree_contents(ROOT / "prompts" / "optimized", prompt_dst / "optimized", dry_run)


def install_claude(home: Path, dry_run: bool) -> None:
    dst = home / ".claude"
    if not dst.is_dir():
        print("SKIP Claude: ~/.claude not found")
        return

    print("\n== Installing Claude assets ==")
    copy_named_dirs(
        ROOT / "skills",
        dst / "skills",
        [
            "android-reverse",
            "analysis-report",
            "final-report",
            "report-analysis-reviewer",
            "project-record-tracker",
        ],
        dry_run,
    )
    copy_tree_contents(ROOT / "agents" / "claude", dst / "agents", dry_run)
    install_prompts(dst, dry_run)


def install_codex(home: Path, dry_run: bool) -> None:
    dst = home / ".codex"
    if not dst.is_dir():
        print("SKIP Codex: ~/.codex not found")
        return

    print("\n== Installing Codex assets ==")
    copy_named_dirs(
        ROOT / "skills",
        dst / "skills",
        [
            "android-reverse",
            "analysis-report",
            "final-report",
            "report-analysis-reviewer",
            "project-record-tracker",
        ],
        dry_run,
    )

    codex_agents = {
        "final-report-agent.md": "final-report.toml",
        "report-analysis-reviewer-agent.md": "report-analysis-reviewer.toml",
    }
    for src_name, dst_name in codex_agents.items():
        copy_file(ROOT / "agents" / "codex" / src_name, dst / "agents" / dst_name, dry_run)

    install_prompts(dst, dry_run)


def install_opencode(home: Path, dry_run: bool) -> None:
    dst = home / ".config" / "opencode"
    if not dst.is_dir():
        print("SKIP opencode: ~/.config/opencode not found")
        return

    print("\n== Installing opencode assets ==")
    copy_named_dirs(
        ROOT / "skills",
        dst / "skills",
        [
            "android-reverse",
            "analysis-report",
            "final-report",
            "report-analysis-reviewer",
            "project-record-tracker",
        ],
        dry_run,
    )
    copy_tree_contents(ROOT / "agents" / "opencode", dst / "agents", dry_run)
    install_prompts(dst, dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(description="Install reverse-analysis workflow assets.")
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without copying files")
    args = parser.parse_args()

    home = Path.home()
    print(f"Source: {ROOT}")
    print(f"Home:   {home}")
    if args.dry_run:
        print("Mode:   dry run")

    install_claude(home, args.dry_run)
    install_codex(home, args.dry_run)
    install_opencode(home, args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
