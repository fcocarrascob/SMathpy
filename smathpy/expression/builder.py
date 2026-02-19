"""Expression builder — fluent API and operator overloading for building SMath RPN expressions."""

from __future__ import annotations

from typing import List, Optional, Union

from .elements import (
    Element,
    bracket,
    function,
    operand,
    operator,
    string_operand,
    unit_operand,
)


# ---------------------------------------------------------------------------
# Expr: a composable, immutable expression tree that renders to RPN
# ---------------------------------------------------------------------------

class Expr:
    """Represents an SMath expression as an ordered list of RPN elements.

    Supports operator overloading so you can write natural Python math::

        x = var("x")
        expr = x ** 2 + 3 * x - 1
    """

    __slots__ = ("_elements",)

    def __init__(self, elements: Optional[List[Element]] = None) -> None:
        self._elements: List[Element] = list(elements) if elements else []

    # -- introspection -------------------------------------------------------

    @property
    def elements(self) -> List[Element]:
        return list(self._elements)

    def __repr__(self) -> str:
        tokens = [e.value for e in self._elements]
        return f"Expr({' '.join(tokens)})"

    # -- combining expressions -----------------------------------------------

    def _binop(self, other: Union[Expr, int, float, str], symbol: str) -> Expr:
        other_expr = _coerce(other)
        return Expr(self._elements + other_expr._elements + [operator(symbol, 2)])

    def _rbinop(self, other: Union[Expr, int, float, str], symbol: str) -> Expr:
        other_expr = _coerce(other)
        return Expr(other_expr._elements + self._elements + [operator(symbol, 2)])

    # arithmetic
    def __add__(self, other):      return self._binop(other, "+")
    def __radd__(self, other):     return self._rbinop(other, "+")
    def __sub__(self, other):      return self._binop(other, "-")
    def __rsub__(self, other):     return self._rbinop(other, "-")
    def __mul__(self, other):      return self._binop(other, "*")
    def __rmul__(self, other):     return self._rbinop(other, "*")
    def __truediv__(self, other):  return self._binop(other, "/")
    def __rtruediv__(self, other): return self._rbinop(other, "/")
    def __pow__(self, other):      return self._binop(other, "^")
    def __rpow__(self, other):     return self._rbinop(other, "^")
    def __neg__(self):             return Expr(self._elements + [operator("-", 1)])

    # comparisons (return Expr, not bool)
    def __gt__(self, other):  return self._binop(other, ">")
    def __lt__(self, other):  return self._binop(other, "<")
    def __ge__(self, other):  return self._binop(other, "≥")
    def __le__(self, other):  return self._binop(other, "≤")

    def neq(self, other) -> Expr:
        """Not-equal comparison (≠). Can't override __ne__ safely."""
        return self._binop(other, "≠")

    def eq(self, other) -> Expr:
        """Equality comparison (=). Can't override __eq__ safely."""
        return self._binop(other, "=")

    def and_(self, other) -> Expr:
        """Logical AND (&)."""
        return self._binop(other, "&")

    # factorial
    def factorial(self) -> Expr:
        return Expr(self._elements + [operator("!", 1)])

    # units
    def __matmul__(self, unit: str) -> Expr:
        """Attach a unit via ``@`` operator: ``5 @ 'm'`` → ``5 * m[unit]``."""
        return Expr(self._elements + [unit_operand(unit), operator("*", 2)])

    # bracket hint
    def grouped(self) -> Expr:
        """Add a bracket display-hint after this expression."""
        return Expr(self._elements + [bracket()])


# ---------------------------------------------------------------------------
# Convenience constructors
# ---------------------------------------------------------------------------

def var(name: str) -> Expr:
    """Create a variable expression."""
    return Expr([operand(name)])


def num(value: Union[int, float]) -> Expr:
    """Create a numeric literal expression."""
    return Expr([operand(value)])


def const(name: str) -> Expr:
    """Create a named constant (π, e, etc.)."""
    return Expr([operand(name)])


def string(value: str) -> Expr:
    """Create a string literal expression."""
    return Expr([string_operand(value)])


def unit(name: str) -> Expr:
    """Create a standalone unit expression."""
    return Expr([unit_operand(name)])


def placeholder() -> Expr:
    """Create a placeholder dot operand."""
    return Expr([operand(".")])


# ---------------------------------------------------------------------------
# Function call helper
# ---------------------------------------------------------------------------

def call(name: str, *args: Union[Expr, int, float, str]) -> Expr:
    """Build a function call expression.

    ``call('abs', x)``  →  ``x abs{1}``
    ``call('el', A, i, j)``  →  ``A i j el{3}``
    """
    elems: list = []
    for a in args:
        elems.extend(_coerce(a)._elements)
    elems.append(function(name, len(args)))
    return Expr(elems)


# ---------------------------------------------------------------------------
# Assignment helpers
# ---------------------------------------------------------------------------

def assign(name: str, value: Union[Expr, int, float, str]) -> Expr:
    """Build an assignment expression: ``name := value``.

    ``assign('x', 5)`` → RPN: ``x 5 :``
    """
    val_expr = _coerce(value)
    return Expr([operand(name)] + val_expr._elements + [operator(":", 2)])


def define(name: str, value: Union[Expr, int, float, str]) -> Expr:
    """Build an equation definition: ``name ≡ value``."""
    val_expr = _coerce(value)
    return Expr([operand(name)] + val_expr._elements + [operator("≡", 2)])


def func_assign(
    name: str, params: List[str], body: Union[Expr, int, float, str]
) -> Expr:
    """Define a user function: ``f(x, y) := body``.

    ``func_assign('f', ['x'], x**2)``
    """
    elems: list = [operand(p) for p in params]
    elems.append(function(name, len(params)))
    elems.extend(_coerce(body)._elements)
    elems.append(operator(":", 2))
    return Expr(elems)


def evaluate(name: str) -> Expr:
    """Simple evaluation expression (just push the variable name)."""
    return Expr([operand(name)])


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _coerce(value: Union[Expr, int, float, str]) -> Expr:
    """Convert a Python value to an Expr if needed."""
    if isinstance(value, Expr):
        return value
    if isinstance(value, (int, float)):
        return num(value)
    if isinstance(value, str):
        return var(value)
    raise TypeError(f"Cannot coerce {type(value).__name__} to Expr")
