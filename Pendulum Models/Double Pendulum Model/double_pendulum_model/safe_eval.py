import ast
import math
from types import CodeType
from typing import ClassVar


class SafeEvaluator:
    """Safely evaluates mathematical expressions using AST validation."""

    _ALLOWED_NODES: ClassVar[set] = {
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
        ast.Attribute,
        ast.BitXor,
    }

    _ALLOWED_MATH_NAMES: ClassVar[dict] = {
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

    def __init__(self, allowed_variables: set[str] | None = None) -> None:
        self.allowed_variables = allowed_variables or set()
        self.allowed_names = {**self._ALLOWED_MATH_NAMES}

    def validate(self, expression: str) -> ast.AST:
        """Parses and validates the expression."""
        parsed = ast.parse(expression.strip(), mode="eval")
        for node in ast.walk(parsed):
            if type(node) not in self._ALLOWED_NODES:
                raise ValueError(f"Disallowed syntax: {type(node).__name__}")
            if isinstance(node, ast.Name) and (
                node.id not in self.allowed_variables and node.id not in self.allowed_names
            ):
                raise ValueError(f"Unknown variable '{node.id}'")
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name | ast.Attribute):
                    raise ValueError("Only direct function calls permitted")
                if isinstance(node.func, ast.Name) and node.func.id not in self.allowed_names:
                    raise ValueError(f"Function '{node.func.id}' not permitted")
        return parsed

    def compile(self, expression: str) -> CodeType:
        """Validates and compiles the expression."""
        parsed = self.validate(expression)
        return compile(parsed, filename="<SafeEvaluator>", mode="eval")

    def evaluate_code(self, code: CodeType, context: dict[str, float] | None = None) -> float:
        """Evaluates compiled code with the given context."""
        eval_context = {**self.allowed_names}
        if context:
            eval_context.update({
                key: value
                for key, value in context.items()
                if key in self.allowed_variables
            })
        return float(eval(code, {"__builtins__": {}}, eval_context))  # noqa: S307

    def evaluate(self, expression: str, context: dict[str, float] | None = None) -> float:
        """Evaluates the expression with the given context."""
        code = self.compile(expression)
        return self.evaluate_code(code, context)
