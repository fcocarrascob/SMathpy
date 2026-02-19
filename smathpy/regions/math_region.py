"""Math region for SMath mathematical expressions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from ..constants import COLOR_BLACK, COLOR_WHITE, FONT_DEFAULT
from ..expression.builder import Expr, assign, evaluate, _coerce
from ..expression.elements import Element, unit_operand, operator
from .base import Region


@dataclass
class MathRegion(Region):
    """A math region containing an RPN expression, optional result, contract, and description.

    Usage::

        # Simple assignment
        region = MathRegion(expr=assign('L', 3) @ 'm')

        # Expression with result
        region = MathRegion(expr=evaluate('GCD'), result_action='numeric', result_elements=[...])

        # With unit conversion on output
        region = MathRegion(expr=evaluate('R.A'), contract_unit='kN')
    """

    expr: Optional[Expr] = None
    optimize: Optional[str] = "2"
    decimal_places: Optional[int] = None
    significant_digits_mode: bool = False
    trailing_zeros: bool = False

    # Result (cached)
    result_action: Optional[str] = None  # "numeric" or "symbolic"
    result_elements: Optional[List[Element]] = None

    # Contract (output unit)
    contract_unit: Optional[str] = None

    # Description (annotation)
    description: Optional[str] = None
    description_texts: Optional[Dict[str, str]] = None
    description_position: str = "Right"
    description_active: bool = True

    @classmethod
    def assignment(cls, name: str, value, unit_name: str = None, **kwargs) -> MathRegion:
        """Create a math region with a simple assignment.

        ``MathRegion.assignment('L', 3, unit_name='m')`` → region with ``L := 3*m``
        """
        expr = assign(name, _coerce(value))
        if unit_name:
            expr = Expr(
                [expr._elements[0]]  # variable name
                + _coerce(value)._elements
                + [unit_operand(unit_name), operator("*", 2)]
                + [expr._elements[-1]]  # assignment operator
            )
        return cls(expr=expr, **kwargs)

    @classmethod
    def evaluation(cls, name: str, contract_unit: str = None, **kwargs) -> MathRegion:
        """Create a math region that evaluates and displays a variable.

        ``MathRegion.evaluation('R.A', contract_unit='kN')``
        """
        return cls(
            expr=evaluate(name),
            contract_unit=contract_unit,
            result_action="numeric",
            **kwargs,
        )

    @classmethod
    def expression(cls, expr: Expr, **kwargs) -> MathRegion:
        """Create a math region from an arbitrary expression."""
        return cls(expr=expr, **kwargs)

    def math_xml_attribs(self) -> dict:
        """Return XML attributes for the <math> element."""
        attribs = {}
        if self.optimize:
            attribs["optimize"] = self.optimize
        if self.decimal_places is not None:
            attribs["decimalPlaces"] = str(self.decimal_places)
        if self.significant_digits_mode:
            attribs["significantDigitsMode"] = "true"
        if self.trailing_zeros:
            attribs["trailingZeros"] = "true"
        return attribs
