"""Plot region for 2D charts and graphs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from ..constants import COLOR_BLACK, COLOR_WHITE
from ..expression.builder import Expr
from .base import Region


@dataclass
class PlotRegion(Region):
    """A plot region for 2D (and potentially 3D) charts.

    Usage::

        plot = PlotRegion(
            inputs=[var('plotter')],
            plot_type='2d',
            render='lines',
        )
    """

    inputs: List[Expr] = field(default_factory=list)
    plot_type: str = "2d"
    render: str = "lines"
    grid: bool = True
    axes: bool = True
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    rotate_x: int = 0
    rotate_y: int = 0
    rotate_z: int = 0
    transpose_x: int = 0
    transpose_y: int = 0
    transpose_z: int = 0
    animate: Optional[str] = None
    show_input_data: bool = True

    def plot_xml_attribs(self) -> dict:
        """Return XML attributes for the <plot> element."""
        attribs = {
            "type": self.plot_type,
            "render": self.render,
            "grid": str(self.grid).lower(),
            "axes": str(self.axes).lower(),
        }
        if self.scale_x != 1.0:
            attribs["scale_x"] = str(self.scale_x)
        if self.scale_y != 1.0:
            attribs["scale_y"] = str(self.scale_y)
        if self.scale_z != 1.0:
            attribs["scale_z"] = str(self.scale_z)
        if self.rotate_x != 0:
            attribs["rotate_x"] = str(self.rotate_x)
        if self.rotate_y != 0:
            attribs["rotate_y"] = str(self.rotate_y)
        if self.rotate_z != 0:
            attribs["rotate_z"] = str(self.rotate_z)
        if self.transpose_x != 0:
            attribs["transpose_x"] = str(self.transpose_x)
        if self.transpose_y != 0:
            attribs["transpose_y"] = str(self.transpose_y)
        if self.transpose_z != 0:
            attribs["transpose_z"] = str(self.transpose_z)
        if self.animate:
            attribs["animate"] = self.animate
        return attribs

    def xml_attribs(self) -> dict:
        """Override to add showInputData."""
        attribs = super().xml_attribs()
        if not self.show_input_data:
            attribs["showInputData"] = "False"
        return attribs
