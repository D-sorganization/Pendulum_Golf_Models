# Sentinel's Journal

## 2025-12-11 - Enforcing Secure Logging Standards
**Vulnerability:** Use of `print` statements instead of structured logging in `python/double_pendulum.py`. This was masked by an explicit ignore rule (`T201`) in `ruff.toml`.
**Learning:** Linter configuration files can hide technical debt and security policy violations. Explicit ignores should be reviewed periodically. `print` statements lack timestamping, log levels, and can clutter standard output in production environments, making incident response harder.
**Prevention:** Remove blanket or file-specific ignores for security-critical rules in linter configs. Enforce logging standards via CI/CD checks.

## 2024-05-22 - Centralized Safe Evaluation
**Vulnerability:** Inconsistent `eval` usage in UI code (`pendulum_pyqt_app.py`) relying only on empty `__builtins__`, which is bypassable.
**Learning:** Security critical logic (like expression evaluation) must be centralized. Copy-pasting leads to degradation of security controls (AST validation was missing in UI copy).
**Prevention:** Create shared security utilities (`SafeEvaluator`) and enforce their usage via linter or code review.
