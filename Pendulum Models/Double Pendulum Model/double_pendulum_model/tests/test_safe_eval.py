import pytest
import math
from double_pendulum_model.safe_eval import SafeEvaluator


def test_safe_eval_basic_math() -> None:
    evaluator = SafeEvaluator("sin(pi/2) + 1")
    assert math.isclose(evaluator(), 2.0)


def test_safe_eval_variables() -> None:
    evaluator = SafeEvaluator("x + y", allowed_variables={"x", "y"})
    assert math.isclose(evaluator({"x": 1.0, "y": 2.0}), 3.0)


def test_safe_eval_rejects_imports() -> None:
    with pytest.raises(ValueError):
        SafeEvaluator("import os")


def test_safe_eval_rejects_builtins() -> None:
    with pytest.raises(ValueError):
        SafeEvaluator("__import__('os').system('ls')")


def test_safe_eval_rejects_attributes() -> None:
    # We disallowed ast.Attribute
    with pytest.raises(ValueError):
        SafeEvaluator("math.sin(0)")


def test_safe_eval_rejects_unknown_variables() -> None:
    with pytest.raises(ValueError):
        SafeEvaluator("z")


def test_safe_eval_rejects_complex_nodes() -> None:
    with pytest.raises(ValueError):
        SafeEvaluator("[x for x in range(10)]")


def test_safe_eval_power_operator() -> None:
    evaluator = SafeEvaluator("2^3")  # ast.BitXor
    # Python ^ is XOR. 2^3 = 1.
    assert evaluator() == 1.0

    # Check if we want to allow **
    evaluator_pow = SafeEvaluator("2**3")
    assert evaluator_pow() == 8.0
