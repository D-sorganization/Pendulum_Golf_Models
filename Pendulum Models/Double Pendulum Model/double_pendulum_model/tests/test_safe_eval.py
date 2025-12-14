import math

import pytest

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
    with pytest.raises(ValueError, match="Invalid syntax"):
        SafeEvaluator("import os")


def test_safe_eval_rejects_builtins() -> None:
    """Test that usage of builtins is rejected."""
    with pytest.raises(ValueError, match="Only direct function calls are permitted"):
        SafeEvaluator("__import__('os').system('ls')")


def test_safe_eval_rejects_attributes() -> None:
    """Test that attribute access is rejected."""
    # We disallowed ast.Attribute
    with pytest.raises(ValueError, match="Only direct function calls are permitted"):
        SafeEvaluator("math.sin(0)")


def test_safe_eval_rejects_unknown_variables() -> None:
    """Test that unknown variables are rejected."""
    with pytest.raises(ValueError, match="Use of unknown variable"):
        SafeEvaluator("z")


def test_safe_eval_rejects_complex_nodes() -> None:
    """Test that complex nodes (like list comprehensions) are rejected."""
    with pytest.raises(ValueError, match="Disallowed syntax"):
        SafeEvaluator("[x for x in range(10)]")


def test_safe_eval_power_operator() -> None:
    """Test that the power operator (^) is rejected to prevent confusion with exponentiation."""
    # Check if we want to allow **
    evaluator_pow = SafeEvaluator("2**3")
    assert evaluator_pow() == 8.0

    # Using ^ should raise a ValueError
    with pytest.raises(ValueError, match="Disallowed syntax"):
        SafeEvaluator("2^3")


def test_safe_eval_prevents_context_override() -> None:
    """Test that context cannot override allowed functions."""
    evaluator = SafeEvaluator("sin(0)")
    # malicious context
    with pytest.raises(ValueError, match="Context cannot override allowed math functions"):
        evaluator({"sin": 100.0})
