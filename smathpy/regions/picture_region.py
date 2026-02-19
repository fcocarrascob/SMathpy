"""Picture region for embedding images."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .base import Region


@dataclass
class PictureRegion(Region):
    """A picture region for embedding base64-encoded images.

    Usage::

        # From file
        pic = PictureRegion.from_file('diagram.png')

        # From raw base64
        pic = PictureRegion(data_base64='iVBORw0KGgo...', format='png')
    """

    data_base64: Optional[str] = None
    format: str = "png"

    @classmethod
    def from_file(cls, path: str, **kwargs) -> PictureRegion:
        """Create a picture region from an image file."""
        p = Path(path)
        with open(p, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")

        fmt = p.suffix.lstrip(".").lower()
        if fmt == "jpg":
            fmt = "jpeg"

        return cls(data_base64=data, format=fmt, **kwargs)

    @classmethod
    def from_bytes(cls, data: bytes, fmt: str = "png", **kwargs) -> PictureRegion:
        """Create a picture region from raw image bytes."""
        return cls(
            data_base64=base64.b64encode(data).decode("ascii"),
            format=fmt,
            **kwargs,
        )
