"""
Omerta Language - Transaction protocol language toolchain.

This package provides tools for parsing, validating, and generating code from
Omerta transaction language (.omt) files.
"""

from .parser import parse, parse_file, load_transaction_ast
from .ast import Schema, Transaction, ActorDecl, MessageDecl, BlockDecl, FunctionDecl
from .validate import validate_schema, ValidationResult, ValidationError

__version__ = "0.1.0"

__all__ = [
    # Parser
    "parse",
    "parse_file",
    "load_transaction_ast",
    # AST
    "Schema",
    "Transaction",
    "ActorDecl",
    "MessageDecl",
    "BlockDecl",
    "FunctionDecl",
    # Validation
    "validate_schema",
    "ValidationResult",
    "ValidationError",
]
