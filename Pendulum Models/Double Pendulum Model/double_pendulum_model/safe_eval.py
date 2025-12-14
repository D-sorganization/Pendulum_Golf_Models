"""
Safe evaluation of user-provided mathematical expressions.
"""

import ast
import math
import typing


class SafeEvaluator:
    """Safe evaluation of user-provided expressions using AST whitelisting."""

    _ALLOWED_NODES: typing.ClassVar[tuple[type, ...]] = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Name,
        ast.Load,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.USub,
        ast.UAdd,
        ast.Call,
        ast.Constant,
        # ast.BitXor is excluded to prevent confusion with exponentiation (^)
    )
    """
    Allowlist of AST node types permitted in user expressions.
    - ast.Expression: Root node.
    - ast.BinOp, ast.UnaryOp: Arithmetic operations.
    - ast.Name, ast.Load: Variable access.
    - ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod: Specific operators.
    - ast.USub, ast.UAdd: Unary operators.
    - ast.Call: Function calls (whitelisted functions only).
    - ast.Constant: Literals.
    """

    _ALLOWED_FUNCTIONS: typing.ClassVar[dict[str, typing.Any]] = {
        name: getattr(math, name)
        for name in (
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "atan2",
            "sqrt",
            "log",
            "log10",
            "exp",
            "pi",
            "tau",
            "fabs",
        )
    }

    def __init__(
        self, expression: str, allowed_variables: set[str] | None = None
    ) -> None:
        """Initialize the SafeEvaluator with an expression and allowed variables."""
        self.expression = expression.strip()
        self.allowed_variables = allowed_variables or set()

        try:
            parsed = ast.parse(self.expression, mode="eval")
        except SyntaxError as e:
            raise ValueError(f"Invalid syntax: {e}") from e

        self._validate_ast(parsed)
        self._code = compile(parsed, filename="SafeEvaluator", mode="eval")

    def __call__(self, context: dict[str, float] | None = None) -> float:
        """Evaluate the expression within the given context."""
        context = context or {}
        safe_context = {**self._ALLOWED_FUNCTIONS, **context}

        # Ensure __builtins__ is not present or is empty
        safe_context.pop("__builtins__", None)

        return float(eval(self._code, {"__builtins__": {}}, safe_context))

    def _validate_ast(self, node: ast.AST) -> None:
        """Validate that the AST only contains allowed nodes and functions."""
        for child in ast.walk(node):
            if not isinstance(child, self._ALLOWED_NODES):
                raise ValueError(
                    f"Disallowed syntax in expression: {type(child).__name__}"
                )

            if (
                isinstance(child, ast.Name)
                and isinstance(child.ctx, ast.Load)
                and child.id not in self._ALLOWED_FUNCTIONS
                and child.id not in self.allowed_variables
            ):
                raise ValueError(f"Use of unknown variable '{child.id}' in expression")

            if isinstance(child, ast.Call):
                if not isinstance(child.func, ast.Name):
                    raise ValueError("Only direct function calls are permitted")
                if child.func.id not in self._ALLOWED_FUNCTIONS:
                    raise ValueError(f"Function '{child.func.id}' is not permitted")
