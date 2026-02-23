"""Control structures: for, while, if, line, range, sum, product."""

from __future__ import annotations

from .builder import Expr, ExprLike, coerce
from .elements import Element, function, operand, operator


# ---------------------------------------------------------------------------
# line block  —  groups N statements
# ---------------------------------------------------------------------------

def line(*statements: ExprLike) -> Expr:
    """Create a ``line`` block that groups multiple statements.

    ``line(stmt1, stmt2, stmt3)`` → RPN: ``stmt1 stmt2 stmt3 3 1 line{5}``

    The last two elements before ``line`` are ``N`` (statement count) and ``1``.
    args = N + 2.
    """
    n = len(statements)
    elems: list = []
    for s in statements:
        elems.extend(coerce(s)._elements)
    elems.append(operand(n))
    elems.append(operand(1))
    elems.append(function("line", n + 2))
    return Expr(elems)


# ---------------------------------------------------------------------------
# range
# ---------------------------------------------------------------------------

def range_(start: ExprLike,
           end: ExprLike,
           step: ExprLike | None = None) -> Expr:
    """SMath ``range`` function.

    ``range_(1, n)`` → ``range(1, n)``
    ``range_(1, n, 2)`` → ``range(1, n, 2)`` (3-arg form)
    """
    if step is None:
        return Expr(
            coerce(start)._elements
            + coerce(end)._elements
            + [function("range", 2)]
        )
    return Expr(
        coerce(start)._elements
        + coerce(end)._elements
        + coerce(step)._elements
        + [function("range", 3)]
    )


# ---------------------------------------------------------------------------
# for loop
# ---------------------------------------------------------------------------

def for_range(var_name: str,
              range_expr: ExprLike,
              body: ExprLike) -> Expr:
    """``for`` loop with range (3-arg form).

    ``for_range('i', range_(1, n), body)``
    → RPN: ``i range_expr body for{3}``
    """
    return Expr(
        [operand(var_name)]
        + coerce(range_expr)._elements
        + coerce(body)._elements
        + [function("for", 3)]
    )


def for_loop(var_name: str,
             start: ExprLike,
             condition: ExprLike,
             increment: ExprLike,
             body: ExprLike) -> Expr:
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
        + coerce(start)._elements
        + [operator(":", 2)]
    )
    cond = coerce(condition)
    incr = Expr(
        [operand(var_name)]
        + coerce(increment)._elements
        + [operator(":", 2)]
    )
    return Expr(
        init._elements + cond._elements + incr._elements
        + coerce(body)._elements
        + [function("for", 4)]
    )


# ---------------------------------------------------------------------------
# while loop
# ---------------------------------------------------------------------------

def while_loop(condition: ExprLike,
               body: ExprLike) -> Expr:
    """``while(condition, body)`` — args=2."""
    return Expr(
        coerce(condition)._elements
        + coerce(body)._elements
        + [function("while", 2)]
    )


# ---------------------------------------------------------------------------
# if conditional
# ---------------------------------------------------------------------------

def if_(condition: ExprLike,
        true_branch: ExprLike,
        false_branch: ExprLike) -> Expr:
    """``if(condition, true, false)`` — args=3."""
    return Expr(
        coerce(condition)._elements
        + coerce(true_branch)._elements
        + coerce(false_branch)._elements
        + [function("if", 3)]
    )


# ---------------------------------------------------------------------------
# sum and product
# ---------------------------------------------------------------------------

def sum_(expr: ExprLike,
         var_name: str,
         start: ExprLike,
         end: ExprLike) -> Expr:
    """``sum(expr, var, start, end)`` — args=4."""
    return Expr(
        coerce(expr)._elements
        + [operand(var_name)]
        + coerce(start)._elements
        + coerce(end)._elements
        + [function("sum", 4)]
    )


def product_(expr: ExprLike,
             var_name: str,
             start: ExprLike,
             end: ExprLike) -> Expr:
    """``product(expr, var, start, end)`` — args=4."""
    return Expr(
        coerce(expr)._elements
        + [operand(var_name)]
        + coerce(start)._elements
        + coerce(end)._elements
        + [function("product", 4)]
    )
