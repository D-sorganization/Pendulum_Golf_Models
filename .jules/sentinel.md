# Sentinel's Journal

## 2025-12-11 - Enforcing Secure Logging Standards
**Vulnerability:** Use of `print` statements instead of structured logging in `python/double_pendulum.py`. This was masked by an explicit ignore rule (`T201`) in `ruff.toml`.
**Learning:** Linter configuration files can hide technical debt and security policy violations. Explicit ignores should be reviewed periodically. `print` statements lack timestamping, log levels, and can clutter standard output in production environments, making incident response harder.
**Prevention:** Remove blanket or file-specific ignores for security-critical rules in linter configs. Enforce logging standards via CI/CD checks.
