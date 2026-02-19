"""RPN expression elements — the atomic building blocks of SMath expressions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Element:
    """Base class for an RPN element (<e> tag in SMath XML)."""

    type: str
    value: str
    args: Optional[int] = None
    style: Optional[str] = None
    preserve: Optional[bool] = None

    def to_xml_attribs(self) -> dict:
        """Return the XML attributes dict for this element."""
        attribs: dict = {"type": self.type}
        if self.style is not None:
            attribs["style"] = self.style
        if self.preserve:
            attribs["preserve"] = "true"
        if self.args is not None:
            attribs["args"] = str(self.args)
        return attribs


def operand(value, style: Optional[str] = None) -> Element:
    """Create an operand element (variable, number, constant)."""
    return Element(type="operand", value=str(value), style=style)


def unit_operand(unit_name: str) -> Element:
    """Create a unit operand element."""
    return Element(type="operand", value=unit_name, style="unit")


def string_operand(value: str) -> Element:
    """Create a string operand element."""
    return Element(type="operand", value=value, style="string")


def operator(symbol: str, args: int) -> Element:
    """Create an operator element."""
    return Element(type="operator", value=symbol, args=args)


def function(name: str, args: int, preserve: Optional[bool] = None) -> Element:
    """Create a function element.

    If *preserve* is None, it is auto-detected from the built-in catalog.
    """
    from ..constants import BUILTIN_FUNCTIONS

    if preserve is None:
        preserve = name in BUILTIN_FUNCTIONS
    return Element(type="function", value=name, args=args, preserve=preserve or None)


def bracket() -> Element:
    """Create a bracket (display hint) element."""
    return Element(type="bracket", value="(")
