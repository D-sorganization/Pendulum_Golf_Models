# Sentinel's Journal

## 2025-12-11 - Enforcing Secure Logging Standards
**Vulnerability:** Use of `print` statements instead of structured logging in `python/double_pendulum.py`. This was masked by an explicit ignore rule (`T201`) in `ruff.toml`.
**Learning:** Linter configuration files can hide technical debt and security policy violations. Explicit ignores should be reviewed periodically. `print` statements lack timestamping, log levels, and can clutter standard output in production environments, making incident response harder.
**Prevention:** Remove blanket or file-specific ignores for security-critical rules in linter configs. Enforce logging standards via CI/CD checks.

## 2025-05-21 - Safe Evaluation of User Expressions
**Vulnerability:** Unsafe use of `eval` with only `__builtins__: {}` restriction in a GUI application allowing arbitrary code execution via crafted inputs.
**Learning:** `eval` with restricted globals is not a sandbox. Python's introspection features (like `__subclasses__`) allow escaping trivial restrictions. Code duplication led to one safe implementation (`ExpressionFunction`) and one unsafe one (`_safe_eval`).
**Prevention:** Use AST-based validation (whitelisting nodes and names) before evaluating expressions. Centralize security-critical logic in a shared utility (`SafeEvaluator`).

## 2025-12-13 - Security Hardening of Expression Evaluation
**Vulnerability:** Previously implemented `SafeEvaluator` was still potentially bypassable via `context` overrides or `__builtins__` leakage.
**Learning:** Defense in depth is required for `eval`. Removing `__builtins__` from globals is good, but ensuring it's not re-injected via locals or `context` is critical. Strict allows-lists (whitelisting) are superior to blocklists. Confusion between `^` (xor) and `**` (pow) can also lead to logic errors if not handled.
**Prevention:** Refactored `SafeEvaluator` to use strict allowed-list for AST nodes (excluding `BitXor` and `Attribute`), ensured explicit removal of `__builtins__`, and prevented context variable shadowing of safe math functions.
