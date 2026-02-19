"""Area region for collapsible sections."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..constants import COLOR_BLACK, COLOR_WHITE
from .base import Region


@dataclass
class AreaRegion(Region):
    """A collapsible area that contains child regions.

    Usage::

        area = AreaRegion(collapsed=True)
        area.add(MathRegion.assignment('x', 5))
        area.add(MathRegion.assignment('y', 10))

    The area will automatically get a terminator region during serialization.
    """

    collapsed: bool = False
    children: List[Region] = field(default_factory=list)

    # Areas only have id, top, color, bgColor (no left/width/height)
    left: int = 0
    width: int = None
    height: int = None

    def add(self, region: Region) -> Region:
        """Add a child region to this collapsible area."""
        self.children.append(region)
        return region
