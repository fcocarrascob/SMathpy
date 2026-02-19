"""Control structures: for, while, if, line, range, sum, product."""

from __future__ import annotations

from typing import List, Union

from .builder import Expr, _coerce
from .elements import Element, function, operand, operator


# ---------------------------------------------------------------------------
# line block  —  groups N statements
# ---------------------------------------------------------------------------

def line(*statements: Union[Expr, int, float, str]) -> Expr:
    """Create a ``line`` block that groups multiple statements.

    ``line(stmt1, stmt2, stmt3)`` → RPN: ``stmt1 stmt2 stmt3 3 1 line{5}``

    The last two elements before ``line`` are ``N`` (statement count) and ``1``.
    args = N + 2.
    """
    n = len(statements)
    elems: list = []
    for s in statements:
        elems.extend(_coerce(s)._elements)
    elems.append(operand(n))
    elems.append(operand(1))
    elems.append(function("line", n + 2))
    return Expr(elems)


# ---------------------------------------------------------------------------
# range
# ---------------------------------------------------------------------------

def range_(start: Union[Expr, int, float, str],
           end: Union[Expr, int, float, str],
           step: Union[Expr, int, float, str, None] = None) -> Expr:
    """SMath ``range`` function.

    ``range_(1, n)`` → ``range(1, n)``
    ``range_(1, n, 2)`` → ``range(1, n, 2)`` (3-arg form)
    """
    if step is None:
        return Expr(
            _coerce(start)._elements
            + _coerce(end)._elements
            + [function("range", 2)]
        )
    return Expr(
        _coerce(start)._elements
        + _coerce(end)._elements
        + _coerce(step)._elements
        + [function("range", 3)]
    )


# ---------------------------------------------------------------------------
# for loop
# ---------------------------------------------------------------------------

def for_range(var_name: str,
              range_expr: Union[Expr, int, float, str],
              body: Union[Expr, int, float, str]) -> Expr:
    """``for`` loop with range (3-arg form).

    ``for_range('i', range_(1, n), body)``
    → RPN: ``i range_expr body for{3}``
    """
    return Expr(
        [operand(var_name)]
        + _coerce(range_expr)._elements
        + _coerce(body)._elements
        + [function("for", 3)]
    )


def for_loop(var_name: str,
             start: Union[Expr, int, float, str],
             condition: Union[Expr, int, float, str],
             increment: Union[Expr, int, float, str],
             body: Union[Expr, int, float, str]) -> Expr:
    """``for`` loop with explicit init/condition/increment (4-arg form).

    Args:
        var_name: Loop variable name.
        start: Initial value (will be wrapped as ``var := start``).
        condition: Loop condition expression.
        increment: Increment expression (will be wrapped as ``var := increment``).
        body: Loop body expression.

    The init is ``var := start``, and increment is ``var := increment_expr``.
    """
    # Build: init_assign condition increment_assign body for{4}
    init = Expr(
        [operand(var_name)]
        + _coerce(start)._elements
        + [operator(":", 2)]
    )
    cond = _coerce(condition)
    incr = Expr(
        [operand(var_name)]
        + _coerce(increment)._elements
        + [operator(":", 2)]
    )
    return Expr(
        init._elements + cond._elements + incr._elements
        + _coerce(body)._elements
        + [function("for", 4)]
    )


# ---------------------------------------------------------------------------
# while loop
# ---------------------------------------------------------------------------

def while_loop(condition: Union[Expr, int, float, str],
               body: Union[Expr, int, float, str]) -> Expr:
    """``while(condition, body)`` — args=2."""
    return Expr(
        _coerce(condition)._elements
        + _coerce(body)._elements
        + [function("while", 2)]
    )


# ---------------------------------------------------------------------------
# if conditional
# ---------------------------------------------------------------------------

def if_(condition: Union[Expr, int, float, str],
        true_branch: Union[Expr, int, float, str],
        false_branch: Union[Expr, int, float, str]) -> Expr:
    """``if(condition, true, false)`` — args=3."""
    return Expr(
        _coerce(condition)._elements
        + _coerce(true_branch)._elements
        + _coerce(false_branch)._elements
        + [function("if", 3)]
    )


# ---------------------------------------------------------------------------
# sum and product
# ---------------------------------------------------------------------------

def sum_(expr: Union[Expr, int, float, str],
         var_name: str,
         start: Union[Expr, int, float, str],
         end: Union[Expr, int, float, str]) -> Expr:
    """``sum(expr, var, start, end)`` — args=4."""
    return Expr(
        _coerce(expr)._elements
        + [operand(var_name)]
        + _coerce(start)._elements
        + _coerce(end)._elements
        + [function("sum", 4)]
    )


def product_(expr: Union[Expr, int, float, str],
             var_name: str,
             start: Union[Expr, int, float, str],
             end: Union[Expr, int, float, str]) -> Expr:
    """``product(expr, var, start, end)`` — args=4."""
    return Expr(
        _coerce(expr)._elements
        + [operand(var_name)]
        + _coerce(start)._elements
        + _coerce(end)._elements
        + [function("product", 4)]
    )
