"""SMath document model and XML serialization."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional, Union

from .constants import (
    APP_PROGID,
    APP_VERSION,
    SMATH_NAMESPACE,
    DEFAULT_LEFT,
    DEFAULT_TOP_START,
    LINE_HEIGHT,
)
from .regions.area_region import AreaRegion
from .regions.base import Region
from .regions.math_region import MathRegion
from .regions.picture_region import PictureRegion
from .regions.plot_region import PlotRegion
from .regions.text_region import TextRegion
from .settings import Settings


class Worksheet:
    """Top-level SMath worksheet document.

    Usage::

        ws = Worksheet(title="My Calculation", author="FCC")
        ws.add(TextRegion.title("Beam Calculation"))
        ws.add(MathRegion.assignment("L", 3, unit_name="m"))
        ws.save("beam.sm")
    """

    def __init__(
        self,
        title: str = "",
        author: str = "",
        lang: str = "eng",
        settings: Optional[Settings] = None,
    ):
        self.settings = settings or Settings()
        if title or author:
            self.settings.set_metadata(lang=lang, title=title, author=author)
        self.regions: List[Region] = []
        self._next_top = DEFAULT_TOP_START
        self._auto_layout = True

    # -- Region management ---------------------------------------------------

    def add(self, region: Region) -> Region:
        """Add a region to the worksheet.

        If the region has no explicit top position set (still at default 9),
        auto-layout places it below the previous region.
        """
        if self._auto_layout and region.top == 9 and len(self.regions) > 0:
            region.top = self._next_top
        if region.left == 0 and not isinstance(region, AreaRegion):
            region.left = DEFAULT_LEFT

        # Estimate height for auto-layout
        h = region.height if region.height else 24
        self._next_top = region.top + h + 3  # 3px gap

        self.regions.append(region)
        return region

    def add_spacing(self, pixels: int = LINE_HEIGHT) -> None:
        """Add vertical spacing before the next region."""
        self._next_top += pixels

    # -- Serialization -------------------------------------------------------

    def to_xml(self) -> ET.ElementTree:
        """Serialize to an ElementTree."""
        # Register namespace to avoid ns0: prefixes
        ET.register_namespace("", SMATH_NAMESPACE)

        root = ET.Element(f"{{{SMATH_NAMESPACE}}}regions")

        # Settings
        self._build_settings(root)

        # Regions
        self._assign_ids()
        for region in self.regions:
            self._build_region(root, region)

        return ET.ElementTree(root)

    def to_xml_string(self) -> str:
        """Serialize to a complete XML string with indentation."""
        tree = self.to_xml()
        root = tree.getroot()

        # Pretty-print with indentation
        _indent_xml(root)

        # Build the XML string manually to include processing instructions
        lines = [
            '<?xml version="1.0" encoding="utf-8" standalone="yes"?>',
            f'<?application progid="{APP_PROGID}" version="{APP_VERSION}"?>',
        ]

        xml_str = ET.tostring(root, encoding="unicode", xml_declaration=False)
        lines.append(xml_str)

        return "\n".join(lines)

    def save(self, path: str) -> None:
        """Save the worksheet to a .sm file."""
        content = self.to_xml_string()
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    # -- Internal XML builders -----------------------------------------------

    def _assign_ids(self) -> None:
        """Assign sequential IDs to all regions."""
        counter = 0
        for region in self.regions:
            region.id = counter
            counter += 1
            if isinstance(region, AreaRegion):
                for child in region.children:
                    child.id = counter
                    counter += 1
                # Terminator ID
                counter += 1  # reserved for terminator

    def _build_settings(self, root: ET.Element) -> None:
        """Build the <settings> element."""
        s = self.settings
        ns = SMATH_NAMESPACE

        settings_el = ET.SubElement(root, f"{{{ns}}}settings")
        settings_el.set("dpi", str(s.dpi))

        # Identity
        identity_el = ET.SubElement(settings_el, f"{{{ns}}}identity")
        id_el = ET.SubElement(identity_el, f"{{{ns}}}id")
        id_el.text = s.doc_id
        rev_el = ET.SubElement(identity_el, f"{{{ns}}}revision")
        rev_el.text = str(s.revision)

        # Metadata
        for meta in s.metadata:
            meta_el = ET.SubElement(settings_el, f"{{{ns}}}metadata")
            meta_el.set("lang", meta.lang)

            if meta.title:
                t = ET.SubElement(meta_el, f"{{{ns}}}title")
                t.text = meta.title
            if meta.author:
                t = ET.SubElement(meta_el, f"{{{ns}}}author")
                t.text = meta.author
            if meta.translator:
                t = ET.SubElement(meta_el, f"{{{ns}}}translator")
                t.text = meta.translator
            if meta.description:
                t = ET.SubElement(meta_el, f"{{{ns}}}description")
                t.text = meta.description
            if meta.company:
                t = ET.SubElement(meta_el, f"{{{ns}}}company")
                t.text = meta.company
            if meta.keywords:
                t = ET.SubElement(meta_el, f"{{{ns}}}keywords")
                t.text = meta.keywords

        # Calculation
        calc_el = ET.SubElement(settings_el, f"{{{ns}}}calculation")
        prec_el = ET.SubElement(calc_el, f"{{{ns}}}precision")
        prec_el.text = str(s.precision)
        exp_el = ET.SubElement(calc_el, f"{{{ns}}}exponentialThreshold")
        exp_el.text = str(s.exponential_threshold)
        frac_el = ET.SubElement(calc_el, f"{{{ns}}}fractions")
        frac_el.text = s.fractions

        # Page model
        pm = s.page_model
        pm_attribs = {
            "active": str(pm.active).lower(),
            "printAreas": str(pm.print_areas).lower(),
            "simpleEqualsOnly": str(pm.simple_equals_only).lower(),
            "printBackgroundImages": str(pm.print_background_images).lower(),
        }
        if pm.view_mode is not None:
            pm_attribs["viewMode"] = pm.view_mode
        if pm.print_grid is not None:
            pm_attribs["printGrid"] = str(pm.print_grid).lower()

        pm_el = ET.SubElement(settings_el, f"{{{ns}}}pageModel", pm_attribs)

        paper_el = ET.SubElement(pm_el, f"{{{ns}}}paper", {
            "id": pm.paper_id,
            "orientation": pm.orientation,
            "width": pm.paper_width,
            "height": pm.paper_height,
        })

        margins_el = ET.SubElement(pm_el, f"{{{ns}}}margins", {
            "left": str(pm.margin_left),
            "right": str(pm.margin_right),
            "top": str(pm.margin_top),
            "bottom": str(pm.margin_bottom),
        })

        header_el = ET.SubElement(pm_el, f"{{{ns}}}header", {
            "alignment": pm.header_alignment,
            "color": pm.header_color,
        })
        header_el.text = pm.header

        footer_el = ET.SubElement(pm_el, f"{{{ns}}}footer", {
            "alignment": pm.footer_alignment,
            "color": pm.footer_color,
        })
        footer_el.text = pm.footer

        bg_el = ET.SubElement(pm_el, f"{{{ns}}}backgrounds")

        # Dependencies
        deps_el = ET.SubElement(settings_el, f"{{{ns}}}dependencies")
        for asm in s.assemblies:
            ET.SubElement(deps_el, f"{{{ns}}}assembly", {
                "name": asm.name,
                "version": asm.version,
                "guid": asm.guid,
            })

    def _build_region(self, parent: ET.Element, region: Region) -> None:
        """Build a <region> element from a region object."""
        ns = SMATH_NAMESPACE

        if isinstance(region, AreaRegion):
            self._build_area_region(parent, region)
        elif isinstance(region, TextRegion):
            self._build_text_region(parent, region)
        elif isinstance(region, MathRegion):
            self._build_math_region(parent, region)
        elif isinstance(region, PlotRegion):
            self._build_plot_region(parent, region)
        elif isinstance(region, PictureRegion):
            self._build_picture_region(parent, region)
        else:
            # Generic region
            ET.SubElement(parent, f"{{{ns}}}region", region.xml_attribs())

    def _build_text_region(self, parent: ET.Element, region: TextRegion) -> None:
        ns = SMATH_NAMESPACE
        region_el = ET.SubElement(parent, f"{{{ns}}}region", region.xml_attribs())

        for lang, text in region.get_texts().items():
            text_el = ET.SubElement(region_el, f"{{{ns}}}text")
            text_el.set("lang", lang)
            p_el = ET.SubElement(text_el, f"{{{ns}}}p")
            if region.bold:
                p_el.set("bold", "true")
            p_el.text = text

    def _build_math_region(self, parent: ET.Element, region: MathRegion) -> None:
        ns = SMATH_NAMESPACE
        region_el = ET.SubElement(parent, f"{{{ns}}}region", region.xml_attribs())

        math_el = ET.SubElement(region_el, f"{{{ns}}}math", region.math_xml_attribs())

        # Description (before input, matching Simpson.sm pattern)
        if region.description_texts:
            for lang, desc_text in region.description_texts.items():
                desc_el = ET.SubElement(math_el, f"{{{ns}}}description")
                desc_el.set("active", str(region.description_active).lower())
                desc_el.set("position", region.description_position)
                desc_el.set("lang", lang)
                p_el = ET.SubElement(desc_el, f"{{{ns}}}p")
                p_el.text = desc_text
        elif region.description:
            desc_el = ET.SubElement(math_el, f"{{{ns}}}description")
            desc_el.set("active", str(region.description_active).lower())
            desc_el.set("position", region.description_position)
            desc_el.set("lang", "eng")
            p_el = ET.SubElement(desc_el, f"{{{ns}}}p")
            p_el.text = region.description

        # Input
        if region.expr:
            input_el = ET.SubElement(math_el, f"{{{ns}}}input")
            for elem in region.expr.elements:
                e_el = ET.SubElement(input_el, f"{{{ns}}}e", elem.to_xml_attribs())
                e_el.text = elem.value

        # Contract (output unit)
        if region.contract_unit:
            contract_el = ET.SubElement(math_el, f"{{{ns}}}contract")
            from .expression.elements import unit_operand as _uo
            uo = _uo(region.contract_unit)
            e_el = ET.SubElement(contract_el, f"{{{ns}}}e", uo.to_xml_attribs())
            e_el.text = uo.value

        # Result
        if region.result_action and region.result_elements:
            result_el = ET.SubElement(math_el, f"{{{ns}}}result")
            result_el.set("action", region.result_action)
            for elem in region.result_elements:
                e_el = ET.SubElement(result_el, f"{{{ns}}}e", elem.to_xml_attribs())
                e_el.text = elem.value

    def _build_plot_region(self, parent: ET.Element, region: PlotRegion) -> None:
        ns = SMATH_NAMESPACE
        region_el = ET.SubElement(parent, f"{{{ns}}}region", region.xml_attribs())

        plot_el = ET.SubElement(region_el, f"{{{ns}}}plot", region.plot_xml_attribs())

        for inp_expr in region.inputs:
            input_el = ET.SubElement(plot_el, f"{{{ns}}}input")
            for elem in inp_expr.elements:
                e_el = ET.SubElement(input_el, f"{{{ns}}}e", elem.to_xml_attribs())
                e_el.text = elem.value

    def _build_picture_region(
        self, parent: ET.Element, region: PictureRegion
    ) -> None:
        ns = SMATH_NAMESPACE
        region_el = ET.SubElement(parent, f"{{{ns}}}region", region.xml_attribs())

        pic_el = ET.SubElement(region_el, f"{{{ns}}}picture")
        raw_el = ET.SubElement(pic_el, f"{{{ns}}}raw", {
            "format": region.format,
            "encoding": "base64",
        })
        raw_el.text = region.data_base64

    def _build_area_region(self, parent: ET.Element, region: AreaRegion) -> None:
        ns = SMATH_NAMESPACE

        # Area regions have limited attributes
        attribs = {
            "id": str(region.id),
            "top": str(region.top),
            "color": region.color,
            "bgColor": region.bg_color,
        }
        region_el = ET.SubElement(parent, f"{{{ns}}}region", attribs)

        # Area start marker
        area_el = ET.SubElement(region_el, f"{{{ns}}}area")
        if region.collapsed:
            area_el.set("collapsed", "true")

        # Child regions inside the area
        for child in region.children:
            self._build_region(region_el, child)

        # Terminator
        term_id = region.id + len(region.children) + 1
        term_attribs = {
            "id": str(term_id),
            "top": str(region.top + 100),
            "color": region.color,
            "bgColor": region.bg_color,
        }
        term_el = ET.SubElement(region_el, f"{{{ns}}}region", term_attribs)
        term_area = ET.SubElement(term_el, f"{{{ns}}}area")
        term_area.set("terminator", "true")


def _indent_xml(elem: ET.Element, level: int = 0) -> None:
    """Add indentation to an ElementTree (in-place).

    Compatible with Python 3.8 (ET.indent was added in 3.9).
    """
    indent = "\n" + "  " * level
    child_indent = "\n" + "  " * (level + 1)

    if len(elem):  # has children
        if not elem.text or not elem.text.strip():
            elem.text = child_indent
        for i, child in enumerate(elem):
            _indent_xml(child, level + 1)
            if i < len(elem) - 1:
                if not child.tail or not child.tail.strip():
                    child.tail = child_indent
            else:
                if not child.tail or not child.tail.strip():
                    child.tail = indent
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = indent
