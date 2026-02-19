"""Base region class for SMath worksheet regions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..constants import COLOR_BLACK, COLOR_WHITE, FONT_DEFAULT


@dataclass
class Region:
    """Base class for all SMath regions.

    Every region has a position (left, top), optional size (width, height),
    and styling attributes (color, bgColor, fontSize, border).
    """

    left: int = 9
    top: int = 9
    width: Optional[int] = None
    height: Optional[int] = None
    color: str = COLOR_BLACK
    bg_color: str = COLOR_WHITE
    font_size: int = FONT_DEFAULT
    border: bool = False
    id: Optional[int] = None  # Assigned during serialization

    def xml_attribs(self) -> dict:
        """Return XML attribute dict for the <region> element."""
        attribs = {
            "id": str(self.id if self.id is not None else 0),
            "left": str(self.left),
            "top": str(self.top),
        }
        if self.width is not None:
            attribs["width"] = str(self.width)
        if self.height is not None:
            attribs["height"] = str(self.height)
        attribs["color"] = self.color
        attribs["bgColor"] = self.bg_color
        if self.font_size != FONT_DEFAULT:
            attribs["fontSize"] = str(self.font_size)
        if self.border:
            attribs["border"] = "true"
        return attribs
