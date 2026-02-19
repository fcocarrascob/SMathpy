"""Tests for the expression builder: RPN generation, operators, functions."""

from smathpy.expression import (
    Expr, var, num, assign, define, func_assign, evaluate, call,
    operand, operator, function,
)


class TestBasicExpressions:
    """Test basic expression building."""

    def test_variable(self):
        x = var("x")
        assert len(x.elements) == 1
        assert x.elements[0].type == "operand"
        assert x.elements[0].value == "x"

    def test_number(self):
        n = num(42)
        assert n.elements[0].value == "42"

    def test_float(self):
        n = num(3.14)
        assert n.elements[0].value == "3.14"


class TestOperators:
    """Test arithmetic and comparison operators."""

    def test_addition(self):
        x = var("x")
        expr = x + 5
        # RPN: x 5 +
        assert len(expr.elements) == 3
        assert expr.elements[0].value == "x"
        assert expr.elements[1].value == "5"
        assert expr.elements[2].value == "+"
        assert expr.elements[2].args == 2

    def test_subtraction(self):
        expr = var("a") - var("b")
        assert expr.elements[2].value == "-"
        assert expr.elements[2].args == 2

    def test_multiplication(self):
        expr = var("x") * 3
        assert expr.elements[2].value == "*"

    def test_division(self):
        expr = var("a") / var("b")
        assert expr.elements[2].value == "/"

    def test_power(self):
        expr = var("x") ** 2
        assert expr.elements[2].value == "^"

    def test_negation(self):
        expr = -var("x")
        assert expr.elements[1].value == "-"
        assert expr.elements[1].args == 1

    def test_comparison_gt(self):
        expr = var("x") > 0
        assert expr.elements[2].value == ">"

    def test_comparison_le(self):
        expr = var("i") <= var("n")
        assert expr.elements[2].value == "≤"

    def test_not_equal(self):
        expr = var("x").neq(0)
        assert expr.elements[2].value == "≠"

    def test_logical_and(self):
        x = var("x")
        y = var("y")
        expr = (x > 0).and_(y > 0)
        assert expr.elements[-1].value == "&"

    def test_complex_expression(self):
        """Test (b-a) / n  →  RPN: b a - n /"""
        b, a, n = var("b"), var("a"), var("n")
        expr = (b - a) / n
        vals = [e.value for e in expr.elements]
        assert vals == ["b", "a", "-", "n", "/"]

    def test_reverse_operations(self):
        """Test 5 + x uses radd."""
        x = var("x")
        expr = 5 + x
        vals = [e.value for e in expr.elements]
        assert vals == ["5", "x", "+"]


class TestAssignment:
    """Test assignment and definition helpers."""

    def test_simple_assign(self):
        """x := 5 → RPN: x 5 :"""
        expr = assign("x", 5)
        vals = [e.value for e in expr.elements]
        assert vals == ["x", "5", ":"]
        assert expr.elements[-1].args == 2

    def test_assign_expression(self):
        """h := (b-a)/n"""
        b, a, n = var("b"), var("a"), var("n")
        expr = assign("h", (b - a) / n)
        vals = [e.value for e in expr.elements]
        assert vals == ["h", "b", "a", "-", "n", "/", ":"]

    def test_define(self):
        """x ≡ expr"""
        expr = define("x", var("a") + var("b"))
        assert expr.elements[-1].value == "≡"

    def test_func_assign(self):
        """f(x) := x^2"""
        x = var("x")
        expr = func_assign("f", ["x"], x ** 2)
        vals = [e.value for e in expr.elements]
        assert vals == ["x", "f", "x", "2", "^", ":"]
        # Function element
        assert expr.elements[1].type == "function"
        assert expr.elements[1].args == 1


class TestFunctionCalls:
    """Test function call building."""

    def test_builtin_call(self):
        """abs(x) → RPN: x abs{1}"""
        expr = call("abs", var("x"))
        assert len(expr.elements) == 2
        assert expr.elements[1].type == "function"
        assert expr.elements[1].value == "abs"
        assert expr.elements[1].args == 1
        assert expr.elements[1].preserve is True  # built-in

    def test_user_function_call(self):
        """f(x, y) → RPN: x y f{2}"""
        expr = call("f", var("x"), var("y"))
        assert expr.elements[-1].preserve is None  # user function

    def test_multi_arg_function(self):
        """el(A, i, j) → RPN: A i j el{3}"""
        expr = call("el", "A", "i", "j")
        assert len(expr.elements) == 4
        assert expr.elements[-1].args == 3


class TestUnitAttachment:
    """Test unit attachment via @ operator."""

    def test_unit_matmul(self):
        """5 @ 'm' → 5 m[unit] *"""
        expr = num(5) @ "m"
        assert len(expr.elements) == 3
        assert expr.elements[1].style == "unit"
        assert expr.elements[1].value == "m"
        assert expr.elements[2].value == "*"

    def test_grouped(self):
        """Test bracket display hint."""
        expr = (var("b") * var("c")).grouped()
        assert expr.elements[-1].type == "bracket"
        assert expr.elements[-1].value == "("
