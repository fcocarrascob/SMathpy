"""Built-in function wrappers for common SMath functions."""

from __future__ import annotations

from typing import Union

from .builder import Expr, call, _coerce


# ---------------------------------------------------------------------------
# Math functions
# ---------------------------------------------------------------------------

def abs_(x: Union[Expr, int, float, str]) -> Expr:
    return call("abs", x)

def sign(x: Union[Expr, int, float, str]) -> Expr:
    return call("sign", x)

def sqrt(x: Union[Expr, int, float, str]) -> Expr:
    return call("sqrt", x)

def exp(x: Union[Expr, int, float, str]) -> Expr:
    return call("exp", x)

def ln(x: Union[Expr, int, float, str]) -> Expr:
    return call("ln", x)

def log(x: Union[Expr, int, float, str]) -> Expr:
    return call("log", x)

def ceil(x: Union[Expr, int, float, str]) -> Expr:
    return call("ceil", x)

def floor(x: Union[Expr, int, float, str]) -> Expr:
    return call("floor", x)

def round_(x: Union[Expr, int, float, str]) -> Expr:
    return call("round", x)

def mod(a: Union[Expr, int, float, str], b: Union[Expr, int, float, str]) -> Expr:
    return call("mod", a, b)

def max_(x: Union[Expr, int, float, str]) -> Expr:
    return call("max", x)

def min_(x: Union[Expr, int, float, str]) -> Expr:
    return call("min", x)


# ---------------------------------------------------------------------------
# Trigonometric functions
# ---------------------------------------------------------------------------

def sin(x: Union[Expr, int, float, str]) -> Expr:
    return call("sin", x)

def cos(x: Union[Expr, int, float, str]) -> Expr:
    return call("cos", x)

def tan(x: Union[Expr, int, float, str]) -> Expr:
    return call("tan", x)

def asin(x: Union[Expr, int, float, str]) -> Expr:
    return call("asin", x)

def acos(x: Union[Expr, int, float, str]) -> Expr:
    return call("acos", x)

def atan(x: Union[Expr, int, float, str]) -> Expr:
    return call("atan", x)


# ---------------------------------------------------------------------------
# Calculus
# ---------------------------------------------------------------------------

def diff(expr: Union[Expr, int, float, str], var: Union[Expr, int, float, str]) -> Expr:
    """First derivative: diff(f, x)."""
    return call("diff", expr, var)

def diff_n(expr: Union[Expr, int, float, str], var: Union[Expr, int, float, str],
           n: Union[Expr, int, float, str]) -> Expr:
    """Nth derivative: diff(f, x, n)."""
    return call("diff", expr, var, n)

def integral(expr: Union[Expr, int, float, str], var: Union[Expr, int, float, str],
             a: Union[Expr, int, float, str], b: Union[Expr, int, float, str]) -> Expr:
    """Definite integral: int(f, x, a, b)."""
    return call("int", expr, var, a, b)


# ---------------------------------------------------------------------------
# String functions
# ---------------------------------------------------------------------------

def concat(a: Union[Expr, int, float, str], b: Union[Expr, int, float, str]) -> Expr:
    return call("concat", a, b)

def num2str(x: Union[Expr, int, float, str]) -> Expr:
    return call("num2str", x)


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def eval_(x: Union[Expr, int, float, str]) -> Expr:
    """Force numeric evaluation."""
    return call("eval", x)
