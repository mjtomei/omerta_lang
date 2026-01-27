# Omerta Language

Transaction protocol language toolchain for Omerta.

## Overview

The Omerta transaction language (`.omt` files) is a domain-specific language for defining cryptographic transaction protocols with state machines, message flows, and actor behaviors.

This package provides:
- **Parser**: PEG-based parser using Lark for `.omt` files
- **Validator**: Semantic validation with typo detection and auto-fix
- **Generators**: Code generation for Python simulations and Markdown documentation

## Installation

```bash
pip install omerta_lang
```

For development:
```bash
pip install -e ".[dev]"
```

## CLI Tools

### omerta-lint

Lint transaction files for errors and warnings:

```bash
omerta-lint protocol/transactions/00_escrow_lock/transaction.omt
omerta-lint --all  # Lint all transaction files
omerta-lint --fix FILE  # Auto-fix obvious typos
```

### omerta-generate

Generate documentation or Python code from a transaction:

```bash
omerta-generate protocol/transactions/00_escrow_lock --markdown
omerta-generate protocol/transactions/00_escrow_lock --python --output-dir simulations/
```

### omerta-regenerate

Regenerate all transaction artifacts:

```bash
omerta-regenerate --verbose
omerta-regenerate --transaction 00_escrow_lock
```

## Library Usage

```python
from omerta_lang import parse, validate_schema

# Parse a transaction file
with open("transaction.omt") as f:
    schema = parse(f.read())

# Validate the schema
result = validate_schema(schema)
for error in result.errors:
    print(f"Error: {error.message}")

# Access AST nodes
for actor in schema.actors:
    print(f"Actor: {actor.name}")
    for state in actor.states:
        print(f"  State: {state.name}")
```

## Environment Variables

- `OMERTA_PROTOCOL_DIR`: Base directory for resolving imports (default: `./protocol`)

## Testing

```bash
pytest
```

## License

MIT
