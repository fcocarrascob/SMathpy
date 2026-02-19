"""Units system for SMath expressions."""

from __future__ import annotations

from ..expression.builder import Expr, _coerce
from ..expression.elements import operator, operand, unit_operand


def with_unit(value, unit_name: str) -> Expr:
    """Attach a unit to a value: ``with_unit(5, 'm')`` → ``5 * m[unit]``."""
    val = _coerce(value)
    return Expr(val._elements + [unit_operand(unit_name), operator("*", 2)])


def power_unit(unit_name: str, exp: int) -> Expr:
    """Build a unit raised to a power: ``power_unit('mm', 2)`` → ``mm²``.

    Produces the RPN: ``[unit(mm), operand(2), ^]``
    Useful as a ``contract_expr`` to display results in e.g. mm² instead of m².

    Example usage::

        from smathpy.units import power_unit
        ws.add(MathRegion(expr=assign('A_s', expr), show_result=True,
                          contract_expr=power_unit('mm', 2)))
    """
    return Expr([unit_operand(unit_name), operand(str(exp)), operator("^", 2)])


def compound_unit(numerator: list, denominator: list = None) -> Expr:
    """Build a compound unit expression.

    ``compound_unit(['kN'], ['m'])`` → ``kN / m``
    ``compound_unit(['m'], ['s', 's'])`` → ``m / s^2`` (via chained division)

    Args:
        numerator: List of unit names in the numerator.
        denominator: List of unit names in the denominator (optional).
    """
    if not numerator:
        raise ValueError("Numerator must have at least one unit")

    elems = [unit_operand(numerator[0])]
    for u in numerator[1:]:
        elems.append(unit_operand(u))
        elems.append(operator("*", 2))

    if denominator:
        for u in denominator:
            elems.append(unit_operand(u))
            elems.append(operator("/", 2))

    return Expr(elems)


def value_with_compound_unit(
    value, numerator: list, denominator: list = None
) -> Expr:
    """Attach a compound unit to a value.

    ``value_with_compound_unit(4, ['kN'], ['m'])`` → ``4 * kN/m``
    """
    val = _coerce(value)
    cu = compound_unit(numerator, denominator)
    return Expr(val._elements + cu._elements + [operator("*", 2)])


# ---------------------------------------------------------------------------
# Common unit shortcuts
# ---------------------------------------------------------------------------

# Length
m = "m"
cm = "cm"
mm = "mm"
km = "km"
dm = "dm"
inch = "in"
ft = "ft"

# Force
N = "N"
kN = "kN"
MN = "MN"
lbf = "lbf"
kgf = "kgf"

# Mass
kg = "kg"
g = "g"
ton = "t"
lb = "lb"

# Time
s = "s"
min_ = "min"
hr = "hr"

# Pressure / Stress
Pa = "Pa"
kPa = "kPa"
MPa = "MPa"
GPa = "GPa"

# Area & Volume (use powers)
# m², m³ etc. are built via expression: var("m") ** 2

# Temperature
K = "K"
degC = "°C"

# Angle
rad = "rad"
deg = "°"
