#!/usr/bin/env python3
"""
Lint Omerta transaction language files for errors and warnings.

Usage:
    omerta-lint <file.omt> [file2.omt ...]
    omerta-lint --all       # Lint all transaction files
    omerta-lint --fix FILE  # Auto-fix obvious typos in FILE
"""

import argparse
import sys
from pathlib import Path

from ..lint import lint_file, find_all_transactions


def main():
    parser = argparse.ArgumentParser(
        description="Lint Omerta transaction language files for errors and warnings."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Files to lint"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Lint all transaction files"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix obvious typos (single-character edits with one suggestion)"
    )
    parser.add_argument(
        "--protocol-dir",
        type=Path,
        default=None,
        help="Protocol directory containing transactions (default: auto-detect)"
    )

    args = parser.parse_args()

    if args.all:
        files = find_all_transactions(args.protocol_dir)
        if not files:
            print("No transaction files found")
            sys.exit(1)
    elif args.files:
        files = [Path(f) for f in args.files]
    else:
        parser.print_help()
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    total_fixable = 0

    for path in files:
        errors, warnings, fixable = lint_file(path, apply_fix=args.fix)
        total_errors += errors
        total_warnings += warnings
        total_fixable += fixable

    if total_errors or total_warnings:
        print(f"\n{total_errors} error(s), {total_warnings} warning(s)")

        # Suggest --fix if there are fixable issues and we didn't already fix
        if total_fixable > 0 and not args.fix:
            if len(files) == 1:
                print(f"\n{total_fixable} issue(s) can be auto-fixed. Run:")
                print(f"  omerta-lint --fix {files[0]}")
            else:
                print(f"\n{total_fixable} issue(s) can be auto-fixed. Run with --fix to apply.")

    sys.exit(1 if total_errors else 0)


if __name__ == "__main__":
    main()
