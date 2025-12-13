import pytest
import math
from double_pendulum_model.safe_eval import SafeEvaluator


def test_safe_eval_basic_math() -> None:
    """Test basic mathematical expressions."""
    evaluator = SafeEvaluator("sin(pi/2) + 1")
    assert math.isclose(evaluator(), 2.0)


def test_safe_eval_variables() -> None:
    """Test evaluation with variables."""
    evaluator = SafeEvaluator("x + y", allowed_variables={"x", "y"})
    assert math.isclose(evaluator({"x": 1.0, "y": 2.0}), 3.0)


def test_safe_eval_rejects_imports() -> None:
    """Test that imports are rejected."""
    with pytest.raises(ValueError):
        SafeEvaluator("import os")


def test_safe_eval_rejects_builtins() -> None:
    """Test that usage of builtins is rejected."""
    with pytest.raises(ValueError):
        SafeEvaluator("__import__('os').system('ls')")


def test_safe_eval_rejects_attributes() -> None:
    """Test that attribute access is rejected."""
    # We disallowed ast.Attribute
    with pytest.raises(ValueError):
        SafeEvaluator("math.sin(0)")


def test_safe_eval_rejects_unknown_variables() -> None:
    """Test that unknown variables are rejected."""
    with pytest.raises(ValueError):
        SafeEvaluator("z")


def test_safe_eval_rejects_complex_nodes() -> None:
    """Test that complex nodes (like list comprehensions) are rejected."""
    with pytest.raises(ValueError):
        SafeEvaluator("[x for x in range(10)]")


def test_safe_eval_power_operator() -> None:
    """Test that the power operator (^) is treated as bitwise XOR (or check behavior)."""
    evaluator = SafeEvaluator("2^3")  # ast.BitXor
    # Python ^ is XOR. 2^3 = 1.
    assert evaluator() == 1.0
