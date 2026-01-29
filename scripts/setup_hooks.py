#!/usr/bin/env python3
"""Configure git to use .githooks directory for hooks."""

import subprocess
import sys
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Failed to configure git hooks: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print("Git hooks path set to .githooks")


if __name__ == "__main__":
    main()
