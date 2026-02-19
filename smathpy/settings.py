"""Document settings model."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .constants import (
    APP_PROGID,
    APP_VERSION,
    ASSEMBLIES,
    DEFAULT_ASSEMBLIES,
    PAPER_A4,
)


@dataclass
class Metadata:
    """Localized metadata for a single language."""

    lang: str = "eng"
    title: str = ""
    author: str = ""
    description: str = ""
    translator: str = ""
    company: str = ""
    keywords: str = ""


@dataclass
class PageModel:
    """Page layout configuration."""

    active: bool = False
    print_areas: bool = True
    simple_equals_only: bool = False
    print_background_images: bool = True
    view_mode: Optional[str] = None
    print_grid: Optional[bool] = None

    paper_id: str = PAPER_A4["id"]
    orientation: str = "Portrait"
    paper_width: str = PAPER_A4["width"]
    paper_height: str = PAPER_A4["height"]

    margin_left: int = 39
    margin_right: int = 39
    margin_top: int = 39
    margin_bottom: int = 39

    header: str = "&[DATE] &[TIME] - &[FILENAME]"
    footer: str = "&[PAGENUM] / &[COUNT]"
    header_alignment: str = "Center"
    footer_alignment: str = "Center"
    header_color: str = "#a9a9a9"
    footer_color: str = "#a9a9a9"


@dataclass
class Assembly:
    """External assembly dependency."""

    name: str
    version: str
    guid: str


@dataclass
class Settings:
    """Complete document settings."""

    # Identity
    doc_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    revision: int = 1

    # Metadata (multiple languages)
    metadata: List[Metadata] = field(default_factory=lambda: [Metadata()])

    # Calculation
    precision: int = 4
    exponential_threshold: int = 5
    fractions: str = "decimal"

    # Page model
    page_model: PageModel = field(default_factory=PageModel)

    # Dependencies
    assemblies: List[Assembly] = field(default_factory=list)

    # Application info
    dpi: int = 96

    def __post_init__(self):
        if not self.assemblies:
            self.assemblies = [
                Assembly(
                    name=name,
                    version=ASSEMBLIES[name]["version"],
                    guid=ASSEMBLIES[name]["guid"],
                )
                for name in DEFAULT_ASSEMBLIES
            ]

    def add_assembly(self, name: str) -> None:
        """Add a known assembly by name."""
        if name in ASSEMBLIES:
            info = ASSEMBLIES[name]
            self.assemblies.append(
                Assembly(name=name, version=info["version"], guid=info["guid"])
            )

    def set_metadata(self, lang: str = "eng", **kwargs) -> None:
        """Set or update metadata for a specific language."""
        for m in self.metadata:
            if m.lang == lang:
                for k, v in kwargs.items():
                    setattr(m, k, v)
                return
        self.metadata.append(Metadata(lang=lang, **kwargs))
