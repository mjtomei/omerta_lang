#!/usr/bin/env python3
"""
Generate documentation and Python code from Omerta transaction definitions.

Usage:
    omerta-generate <tx_dir> [--markdown] [--python] [--output-dir <dir>]

Example:
    omerta-generate protocol/transactions/00_escrow_lock --markdown
    omerta-generate protocol/transactions/00_escrow_lock --python --output-dir simulations/transactions
"""

import argparse
import sys
from pathlib import Path

from ..generators.python import generate_markdown, generate_python


def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation and Python code from transaction definitions"
    )
    parser.add_argument("tx_dir", help="Directory containing transaction.omt")
    parser.add_argument("--markdown", action="store_true", help="Generate markdown documentation")
    parser.add_argument("--python", action="store_true", help="Generate Python code")
    parser.add_argument("--output-dir", help="Output directory")

    args = parser.parse_args()

    tx_dir = Path(args.tx_dir)
    if not tx_dir.exists():
        print(f"Error: Directory not found: {tx_dir}", file=sys.stderr)
        sys.exit(1)

    if args.markdown:
        output_dir = Path(args.output_dir) if args.output_dir else tx_dir.parent
        tx_name = tx_dir.name
        output_path = output_dir / f"{tx_name}.md"
        generate_markdown(tx_dir, output_path)
        print(f"Generated: {output_path}")

    if args.python:
        output_dir = Path(args.output_dir) if args.output_dir else Path("simulations/transactions")
        tx_name = tx_dir.name.split("_", 1)[1] if "_" in tx_dir.name else tx_dir.name
        output_path = output_dir / f"{tx_name}_generated.py"
        generate_python(tx_dir, output_path)
        print(f"Generated: {output_path}")

    if not args.markdown and not args.python:
        print("Specify --markdown and/or --python to generate output")
        sys.exit(1)


if __name__ == "__main__":
    main()
