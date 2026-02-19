"""Region package — all SMath region types."""

from .area_region import AreaRegion
from .base import Region
from .math_region import MathRegion
from .picture_region import PictureRegion
from .plot_region import PlotRegion
from .text_region import TextRegion

__all__ = [
    "Region",
    "TextRegion",
    "MathRegion",
    "PlotRegion",
    "PictureRegion",
    "AreaRegion",
]
