#!/usr/bin/env python3
"""Read-only structural validation, independent of the source checkout and MCP host."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def headings(text):
    seen = {}
    result = set()
    fenced = False
    for line in text.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        slug = re.sub(r"[^\w\s-]", "", match[1].casefold())
        slug = re.sub(r"\s", "-", slug)
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        result.add(slug if not n else slug + "-" + str(n))
    return result


def contained(path):
    try:
        path.resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def validate():
    errors = []
    entry = ROOT / "SKILL.md"
    text = entry.read_text(encoding="utf-8")
    front = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not front or not re.search(r"(?m)^name: android-reverse$", front[1]):
        errors.append("missing or wrong skill frontmatter")
    if not front or not re.search(r"(?m)^description:\s*\S", front[1]):
        errors.append("missing description")
    documents = [entry, *sorted((ROOT / "reference").rglob("*.md"))]
    cache = {p.resolve(): p.read_text(encoding="utf-8") for p in documents}
    graph = {p: set() for p in cache}
    link_count = 0
    for document, body in cache.items():
        if "\u201c" in body or "\u201d" in body:
            errors.append(str(document.relative_to(ROOT)) + ": forbidden quote")
        fence_count = sum(bool(re.match(r"^\s*```", line)) for line in body.splitlines())
        if fence_count % 2:
            errors.append(str(document.relative_to(ROOT)) + ": unmatched fence")
        for match in re.finditer(r"\[[^\]\n]+\]\(([^)\n]+)\)", body):
            raw = match[1].strip().strip("<>")
            if urlsplit(raw).scheme:
                continue
            relative, _, fragment = raw.partition("#")
            target = (document.parent / unquote(relative)).resolve() if relative else document
            link_count += 1
            if not contained(target):
                errors.append(f"{document.name}: link leaves skill: {raw}")
            elif not target.exists():
                errors.append(f"{document.name}: missing link: {raw}")
            elif fragment and target.suffix == ".md":
                target_body = cache.get(target)
                if target_body is None:
                    target_body = target.read_text(encoding="utf-8")
                if unquote(fragment).casefold() not in headings(target_body):
                    errors.append(f"{document.name}: missing heading: {raw}")
            if target in cache:
                graph[document].add(target)
        for raw in re.findall(r"`(reference/[a-z0-9_./-]+\.md)`", body):
            if not (ROOT / raw).is_file():
                errors.append("missing entrypoint reference: " + raw)
    manifest_path = ROOT / "maintenance" / "migration.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key, count in (("references", 67), ("code", 65)):
        rows = manifest[key]
        sources = [row["source"] for row in rows]
        if len(rows) != count or len(set(sources)) != count:
            errors.append(f"migration {key}: incomplete or duplicate inventory")
        for row in rows:
            if not row.get("decision") or not row.get("reason") or not row.get("targets"):
                errors.append("missing migration disposition: " + row["source"])
            for relative in row["targets"]:
                target = ROOT / relative
                if not contained(target) or not target.is_file():
                    errors.append("missing migration target: " + relative)
    for path in sorted((ROOT / "scripts" / "offline").glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"syntax: {path.name}: {exc}")
    if not (ROOT / "scripts" / "offline" / "LICENSE.apk-reverse").is_file():
        errors.append("missing upstream license")
    reachable = set()
    queue = [entry.resolve()]
    while queue:
        current = queue.pop()
        if current not in reachable:
            reachable.add(current)
            queue.extend(graph.get(current, ()))
    for orphan in set(cache) - reachable:
        errors.append("unreachable reference: " + str(orphan.relative_to(ROOT)))
    return errors, len(documents), link_count


if __name__ == "__main__":
    try:
        problems, docs, links = validate()
    except (OSError, ValueError, KeyError) as exc:
        print("validation error:", exc, file=sys.stderr)
        sys.exit(1)
    for problem in problems:
        print("ERROR:", problem)
    print("documents=%d links=%d errors=%d" % (docs, links, len(problems)))
    print("entrypoint_bytes=%d" % (ROOT / "SKILL.md").stat().st_size)
    sys.exit(bool(problems))
