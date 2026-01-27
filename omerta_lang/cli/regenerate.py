#!/usr/bin/env python3
"""
Regenerate all transaction artifacts from Omerta language files.

This script regenerates:
1. Markdown documentation
2. Python simulation code

Usage:
    omerta-regenerate [--verbose] [--transaction TX_NAME]
"""

import argparse
import os
import sys
from pathlib import Path

from ..generators.python import generate_markdown, generate_python


def find_transaction_dirs(protocol_dir: Path) -> list[Path]:
    """Find all transaction directories containing .omt files."""
    transactions_dir = protocol_dir / "transactions"
    if not transactions_dir.exists():
        return []

    tx_dirs = []
    for item in sorted(transactions_dir.iterdir()):
        if item.is_dir() and item.name != "graphs":
            omt_file = item / "transaction.omt"
            if omt_file.exists():
                tx_dirs.append(item)
    return tx_dirs


def regenerate_markdown(tx_dir: Path, output_dir: Path, verbose: bool = False) -> bool:
    """Regenerate markdown documentation for a transaction."""
    tx_name = tx_dir.name
    output_path = output_dir / f"{tx_name}.md"

    try:
        generate_markdown(tx_dir, output_path)
        if verbose:
            print(f"  Generated: {output_path}")
        return True
    except Exception as e:
        print(f"  Error generating markdown: {e}", file=sys.stderr)
        return False


def regenerate_python(tx_dir: Path, output_dir: Path, verbose: bool = False) -> bool:
    """Regenerate Python simulation code for a transaction."""
    tx_name = tx_dir.name.split("_", 1)[1] if "_" in tx_dir.name else tx_dir.name
    output_path = output_dir / f"{tx_name}_generated.py"

    try:
        generate_python(tx_dir, output_path)
        if verbose:
            print(f"  Generated: {output_path}")
        return True
    except Exception as e:
        print(f"  Error generating Python: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate all transaction artifacts from Omerta language files"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output",
    )
    parser.add_argument(
        "--transaction", "-t",
        help="Only process specific transaction (e.g., '00_escrow_lock')",
    )
    parser.add_argument(
        "--protocol-dir",
        type=Path,
        default=None,
        help="Protocol directory (default: ./protocol or OMERTA_PROTOCOL_DIR env var)",
    )
    parser.add_argument(
        "--python-output",
        type=Path,
        default=None,
        help="Python output directory (default: ./simulations/transactions)",
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="Only regenerate markdown documentation",
    )
    parser.add_argument(
        "--python-only",
        action="store_true",
        help="Only regenerate Python code",
    )

    args = parser.parse_args()

    # Determine directories
    protocol_dir = args.protocol_dir
    if protocol_dir is None:
        protocol_dir = Path(os.environ.get("OMERTA_PROTOCOL_DIR", "./protocol"))

    python_output = args.python_output
    if python_output is None:
        python_output = Path("./simulations/transactions")

    # Find transaction directories
    tx_dirs = find_transaction_dirs(protocol_dir)

    if not tx_dirs:
        print(f"No transaction directories found in {protocol_dir}/transactions", file=sys.stderr)
        sys.exit(1)

    # Filter to specific transaction if requested
    if args.transaction:
        tx_dirs = [d for d in tx_dirs if d.name == args.transaction]
        if not tx_dirs:
            print(f"Transaction not found: {args.transaction}", file=sys.stderr)
            sys.exit(1)

    print(f"Found {len(tx_dirs)} transaction(s)")
    print()

    success_count = 0
    error_count = 0

    for tx_dir in tx_dirs:
        print(f"Processing: {tx_dir.name}")

        md_ok = True
        py_ok = True

        if not args.python_only:
            md_ok = regenerate_markdown(tx_dir, tx_dir.parent, args.verbose)

        if not args.markdown_only:
            py_ok = regenerate_python(tx_dir, python_output, args.verbose)

        if md_ok and py_ok:
            success_count += 1
        else:
            error_count += 1

        print()

    print(f"Done: {success_count} succeeded, {error_count} failed")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
