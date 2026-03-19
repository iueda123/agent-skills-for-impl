#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


def run_gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "gh command failed"
        raise SystemExit(message)
    return result.stdout


def slugify(text: str) -> str:
    ascii_text = text.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return slug or "issue"


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
    if not content.startswith("---\n"):
        raise SystemExit("markdown file must start with YAML frontmatter")

    end = content.find("\n---\n", 4)
    if end == -1:
        raise SystemExit("frontmatter closing delimiter not found")

    header = content[4:end]
    body = content[end + 5 :]
    data: dict[str, str] = {}
    for raw_line in header.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise SystemExit(f"invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data, body


def find_issue_markdown_paths(number: int, out_dir: str) -> list[Path]:
    issue_dir = Path(out_dir) / str(number)
    if not issue_dir.exists():
        return []
    return sorted(issue_dir.glob("*.md"))


def list_issues(state: str, limit: int, repo: str | None) -> None:
    args = [
        "issue",
        "list",
        "--state",
        state,
        "--limit",
        str(limit),
        "--json",
        "number,title,state,updatedAt",
    ]
    if repo:
        args.extend(["--repo", repo])

    issues = json.loads(run_gh(args))
    if not issues:
        print("No issues found.")
        return

    print(f"{'NUMBER':>6}  {'STATE':<6}  {'UPDATED':<20}  TITLE")
    for issue in issues:
        updated = issue["updatedAt"].replace("T", " ").replace("Z", "")
        print(f"{issue['number']:>6}  {issue['state']:<6}  {updated:<20}  {issue['title']}")


def show_local_paths(number: int, out_dir: str) -> None:
    paths = find_issue_markdown_paths(number, out_dir)
    if not paths:
        print("No local markdown found.")
        return
    for path in paths:
        print(path)


def fetch_issue(number: int, out_dir: str, repo: str | None, overwrite: bool) -> None:
    existing_paths = find_issue_markdown_paths(number, out_dir)
    if existing_paths and not overwrite:
        existing_text = "\n".join(str(path) for path in existing_paths)
        raise SystemExit(
            "local markdown already exists for this issue:\n"
            f"{existing_text}\n"
            "reuse it or rerun fetch with --overwrite"
        )

    args = [
        "issue",
        "view",
        str(number),
        "--json",
        "number,title,body,url",
    ]
    if repo:
        args.extend(["--repo", repo])

    issue = json.loads(run_gh(args))
    issue_dir = Path(out_dir) / str(issue["number"])
    issue_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(issue['title'])}.md"
    path = issue_dir / filename

    if overwrite:
        for existing_path in existing_paths:
            if existing_path != path and existing_path.exists():
                existing_path.unlink()

    body = issue.get("body") or ""
    content = (
        "---\n"
        f"number: {issue['number']}\n"
        f"title: {issue['title']}\n"
        f"url: {issue['url']}\n"
        "---\n"
        f"{body}"
    )
    path.write_text(content, encoding="utf-8")
    print(path)


def push_issue(path_str: str, repo: str | None) -> None:
    path = Path(path_str)
    if not path.exists():
        raise SystemExit(f"file not found: {path}")

    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    number = meta.get("number")
    title = meta.get("title")
    if not number or not title:
        raise SystemExit("frontmatter must contain number and title")

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(body.lstrip("\n"))
        temp_path = tmp.name

    try:
        args = [
            "issue",
            "edit",
            number,
            "--title",
            title,
            "--body-file",
            temp_path,
        ]
        if repo:
            args.extend(["--repo", repo])
        run_gh(args)
    finally:
        os.unlink(temp_path)

    print(f"Updated issue #{number} from {path}")
    path.unlink()

    parent = path.parent
    if parent.exists() and not any(parent.iterdir()):
        parent.rmdir()
    print(f"Deleted local markdown: {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export and sync GitHub issues as markdown files.")
    parser.add_argument("--repo", help="Optional [HOST/]OWNER/REPO target.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List issues.")
    list_parser.add_argument("--state", default="open", choices=["open", "closed", "all"])
    list_parser.add_argument("--limit", type=int, default=30)

    local_parser = subparsers.add_parser("local", help="Show local markdown paths for one issue.")
    local_parser.add_argument("number", type=int)
    local_parser.add_argument("--out-dir", default="gh-issues")

    fetch_parser = subparsers.add_parser("fetch", help="Export one issue to markdown.")
    fetch_parser.add_argument("number", type=int)
    fetch_parser.add_argument("--out-dir", default="gh-issues")
    fetch_parser.add_argument("--overwrite", action="store_true")

    push_parser = subparsers.add_parser("push", help="Push markdown changes back to GitHub.")
    push_parser.add_argument("path")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        list_issues(args.state, args.limit, args.repo)
        return
    if args.command == "local":
        show_local_paths(args.number, args.out_dir)
        return
    if args.command == "fetch":
        fetch_issue(args.number, args.out_dir, args.repo, args.overwrite)
        return
    if args.command == "push":
        push_issue(args.path, args.repo)
        return
    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
