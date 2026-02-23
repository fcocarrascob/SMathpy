"""Built-in function wrappers for common SMath functions."""

from __future__ import annotations

from .builder import Expr, ExprLike, call


# ---------------------------------------------------------------------------
# Math functions
# ---------------------------------------------------------------------------

def abs_(x: ExprLike) -> Expr:
    """Absolute value."""
    return call("abs", x)

def sign(x: ExprLike) -> Expr:
    """Sign of x (-1, 0, or 1)."""
    return call("sign", x)

def sqrt(x: ExprLike) -> Expr:
    """Square root."""
    return call("sqrt", x)

def exp(x: ExprLike) -> Expr:
    """Exponential function (e^x)."""
    return call("exp", x)

def ln(x: ExprLike) -> Expr:
    """Natural logarithm."""
    return call("ln", x)

def log(x: ExprLike) -> Expr:
    """Base-10 logarithm."""
    return call("log", x)

def ceil(x: ExprLike) -> Expr:
    """Ceiling (round up to integer)."""
    return call("ceil", x)

def floor(x: ExprLike) -> Expr:
    """Floor (round down to integer)."""
    return call("floor", x)

def round_(x: ExprLike) -> Expr:
    """Round to nearest integer."""
    return call("round", x)

def mod(a: ExprLike, b: ExprLike) -> Expr:
    """Modulo (remainder of a / b)."""
    return call("mod", a, b)

def max_(*args: ExprLike) -> Expr:
    """Maximum of the given values."""
    return call("max", *args)

def min_(*args: ExprLike) -> Expr:
    """Minimum of the given values."""
    return call("min", *args)


# ---------------------------------------------------------------------------
# Trigonometric functions
# ---------------------------------------------------------------------------

def sin(x: ExprLike) -> Expr:
    """Sine."""
    return call("sin", x)

def cos(x: ExprLike) -> Expr:
    """Cosine."""
    return call("cos", x)

def tan(x: ExprLike) -> Expr:
    """Tangent."""
    return call("tan", x)

def asin(x: ExprLike) -> Expr:
    """Arcsine (inverse sine)."""
    return call("asin", x)

def acos(x: ExprLike) -> Expr:
    """Arccosine (inverse cosine)."""
    return call("acos", x)

def atan(x: ExprLike) -> Expr:
    """Arctangent (inverse tangent)."""
    return call("atan", x)


# ---------------------------------------------------------------------------
# Calculus
# ---------------------------------------------------------------------------

def diff(expr: ExprLike, var: ExprLike) -> Expr:
    """First derivative: diff(f, x)."""
    return call("diff", expr, var)

def diff_n(expr: ExprLike, var: ExprLike,
           n: ExprLike) -> Expr:
    """Nth derivative: diff(f, x, n)."""
    return call("diff", expr, var, n)

def integral(expr: ExprLike, var: ExprLike,
             a: ExprLike, b: ExprLike) -> Expr:
    """Definite integral: int(f, x, a, b)."""
    return call("int", expr, var, a, b)


# ---------------------------------------------------------------------------
# String functions
# ---------------------------------------------------------------------------

def concat(a: ExprLike, b: ExprLike) -> Expr:
    """String concatenation."""
    return call("concat", a, b)

def num2str(x: ExprLike) -> Expr:
    """Convert number to string."""
    return call("num2str", x)


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def eval_(x: ExprLike) -> Expr:
    """Force numeric evaluation."""
    return call("eval", x)
