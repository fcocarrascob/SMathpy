"""smathpy — Python API for programmatic generation of SMath Studio (.sm) files."""

__version__ = "0.1.0"

from .document import Worksheet
from .regions import (
    AreaRegion,
    MathRegion,
    PictureRegion,
    PlotRegion,
    Region,
    TextRegion,
)
from .settings import Assembly, Metadata, PageModel, Settings
from .expression import (
    Expr,
    assign,
    call,
    const,
    define,
    evaluate,
    func_assign,
    num,
    placeholder,
    string,
    unit,
    var,
)

__all__ = [
    # Core
    "Worksheet",
    # Regions
    "Region", "TextRegion", "MathRegion", "PlotRegion", "PictureRegion", "AreaRegion",
    # Settings
    "Settings", "Metadata", "PageModel", "Assembly",
    # Expression
    "Expr", "var", "num", "const", "string", "unit", "placeholder",
    "assign", "define", "func_assign", "evaluate", "call",
]
