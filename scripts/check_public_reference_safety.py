#!/usr/bin/env python3
"""Offline checks for secret-shaped values and unexpected AWS account IDs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".py", ".tf", ".yaml", ".yml", ".json", ".sh", ".txt"}
EXCLUDED_DIRS = {".git", ".terraform", "node_modules", "vendor"}
ALLOWED_AWS_ACCOUNT_IDS = {"111122223333", "123456789012"}

SECRET_PATTERNS = (
    ("AWS access key ID", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)
AWS_ACCOUNT_ID = re.compile(r"(?<!\d)(\d{12})(?!\d)")


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def check_file(path: Path, root: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    display_path = path.relative_to(root)
    findings: list[str] = []

    for label, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(f"{display_path}:{line_number(text, match.start())}: {label}")

    for match in AWS_ACCOUNT_ID.finditer(text):
        account_id = match.group(1)
        if account_id not in ALLOWED_AWS_ACCOUNT_IDS:
            findings.append(
                f"{display_path}:{line_number(text, match.start())}: unexpected AWS account ID"
            )

    return findings


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    findings: list[str] = []

    for path in iter_text_files(root):
        findings.extend(check_file(path, root))

    if findings:
        print("Public-reference safety check failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        print("Matched values are intentionally not printed.", file=sys.stderr)
        return 1

    print("Public-reference safety check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
