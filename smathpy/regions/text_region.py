"""Text region for multilingual text content."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from ..constants import COLOR_BLACK, COLOR_BLUE, COLOR_WHITE, FONT_DEFAULT, FONT_TITLE
from .base import Region


@dataclass
class TextRegion(Region):
    """A text region supporting multilingual paragraphs.

    Usage::

        # Simple single-language text
        region = TextRegion(text="Hello World")

        # Bold blue title
        region = TextRegion.title("My Calculation")

        # Section divider
        region = TextRegion.section("Input data:")

        # Multilingual text
        region = TextRegion(
            texts={"eng": "Hello", "rus": "Привет", "ind": "Halo"},
            bold=True
        )
    """

    text: Optional[str] = None
    texts: Optional[Dict[str, str]] = None
    bold: bool = False
    lang: str = "eng"

    def get_texts(self) -> Dict[str, str]:
        """Return the multilingual text dict."""
        if self.texts:
            return self.texts
        if self.text is not None:
            return {self.lang: self.text}
        return {}

    @classmethod
    def title(cls, text: str, lang: str = "eng", **kwargs) -> TextRegion:
        """Create a title text region (bold, blue, larger font)."""
        return cls(
            text=text,
            bold=True,
            color=COLOR_BLUE,
            font_size=FONT_TITLE,
            lang=lang,
            **kwargs,
        )

    @classmethod
    def section(cls, text: str, lang: str = "eng", **kwargs) -> TextRegion:
        """Create a section divider (bordered, gray background)."""
        return cls(
            text=text,
            border=True,
            color=COLOR_BLACK,
            bg_color="#dddddd",
            lang=lang,
            **kwargs,
        )
