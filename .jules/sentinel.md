# Sentinel's Journal

## 2025-12-11 - Enforcing Secure Logging Standards
**Vulnerability:** Use of `print` statements instead of structured logging in `python/double_pendulum.py`. This was masked by an explicit ignore rule (`T201`) in `ruff.toml`.
**Learning:** Linter configuration files can hide technical debt and security policy violations. Explicit ignores should be reviewed periodically. `print` statements lack timestamping, log levels, and can clutter standard output in production environments, making incident response harder.
**Prevention:** Remove blanket or file-specific ignores for security-critical rules in linter configs. Enforce logging standards via CI/CD checks.

## 2025-05-21 - Safe Evaluation of User Expressions
**Vulnerability:** Unsafe use of `eval` with only `__builtins__: {}` restriction in a GUI application allowing arbitrary code execution via crafted inputs.
**Learning:** `eval` with restricted globals is not a sandbox. Python's introspection features (like `__subclasses__`) allow escaping trivial restrictions. Code duplication led to one safe implementation (`ExpressionFunction`) and one unsafe one (`_safe_eval`).
**Prevention:** Use AST-based validation (whitelisting nodes and names) before evaluating expressions. Centralize security-critical logic in a shared utility (`SafeEvaluator`).
