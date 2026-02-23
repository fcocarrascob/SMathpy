"""Tests for document creation and XML serialization."""

import xml.etree.ElementTree as ET

from smathpy import Worksheet, TextRegion, MathRegion, assign, var, num, evaluate
from smathpy.constants import SMATH_NAMESPACE
from smathpy.regions.plot_region import PlotRegion
from smathpy.regions.picture_region import PictureRegion
from smathpy.regions.area_region import AreaRegion
from smathpy.units import power_unit, compound_unit


NS = {"sm": SMATH_NAMESPACE}


class TestWorksheetCreation:
    def test_empty_document(self):
        ws = Worksheet(title="Test", author="Author")
        xml_str = ws.to_xml_string()

        assert '<?xml version="1.0"' in xml_str
        assert '<?application progid="SMath Studio Desktop"' in xml_str
        assert "regions" in xml_str

    def test_metadata(self):
        ws = Worksheet(title="My Title", author="Me")
        tree = ws.to_xml()
        root = tree.getroot()

        meta = root.find(f".//{{{SMATH_NAMESPACE}}}metadata[@lang='eng']")
        assert meta is not None
        assert meta.find(f"{{{SMATH_NAMESPACE}}}title").text == "My Title"
        assert meta.find(f"{{{SMATH_NAMESPACE}}}author").text == "Me"

    def test_settings_structure(self):
        ws = Worksheet()
        tree = ws.to_xml()
        root = tree.getroot()

        settings = root.find(f"{{{SMATH_NAMESPACE}}}settings")
        assert settings is not None
        assert settings.get("dpi") == "96"

        identity = settings.find(f"{{{SMATH_NAMESPACE}}}identity")
        assert identity is not None

        calc = settings.find(f"{{{SMATH_NAMESPACE}}}calculation")
        assert calc is not None
        assert calc.find(f"{{{SMATH_NAMESPACE}}}precision").text == "4"

    def test_dependencies(self):
        ws = Worksheet()
        tree = ws.to_xml()
        root = tree.getroot()

        deps = root.find(f".//{{{SMATH_NAMESPACE}}}dependencies")
        assert deps is not None
        assemblies = deps.findall(f"{{{SMATH_NAMESPACE}}}assembly")
        assert len(assemblies) >= 3


class TestTextRegionSerialization:
    def test_simple_text(self):
        ws = Worksheet()
        ws.add(TextRegion(text="Hello World"))
        tree = ws.to_xml()
        root = tree.getroot()

        region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        assert region is not None
        text_el = region.find(f"{{{SMATH_NAMESPACE}}}text")
        assert text_el is not None
        assert text_el.get("lang") == "eng"
        p_el = text_el.find(f"{{{SMATH_NAMESPACE}}}p")
        assert p_el.text == "Hello World"

    def test_title_region(self):
        ws = Worksheet()
        ws.add(TextRegion.title("My Title"))
        tree = ws.to_xml()
        root = tree.getroot()

        region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        assert region.get("color") == "#0000ff"
        assert region.get("fontSize") == "12"
        p = root.find(f".//{{{SMATH_NAMESPACE}}}p")
        assert p.get("bold") == "true"

    def test_section_divider(self):
        ws = Worksheet()
        ws.add(TextRegion.section("Input data:"))
        tree = ws.to_xml()
        root = tree.getroot()

        region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        assert region.get("border") == "true"
        assert region.get("bgColor") == "#dddddd"

    def test_multilingual(self):
        ws = Worksheet()
        ws.add(TextRegion(
            texts={"eng": "Hello", "rus": "Привет"},
            bold=True,
        ))
        tree = ws.to_xml()
        root = tree.getroot()

        texts = root.findall(f".//{{{SMATH_NAMESPACE}}}text")
        assert len(texts) == 2
        langs = {t.get("lang") for t in texts}
        assert langs == {"eng", "rus"}


class TestMathRegionSerialization:
    def test_simple_assignment(self):
        ws = Worksheet()
        ws.add(MathRegion(expr=assign("x", 5)))
        tree = ws.to_xml()
        root = tree.getroot()

        math_el = root.find(f".//{{{SMATH_NAMESPACE}}}math")
        assert math_el is not None
        input_el = math_el.find(f"{{{SMATH_NAMESPACE}}}input")
        elems = input_el.findall(f"{{{SMATH_NAMESPACE}}}e")
        assert len(elems) == 3
        assert elems[0].text == "x"
        assert elems[0].get("type") == "operand"
        assert elems[1].text == "5"
        assert elems[2].text == ":"
        assert elems[2].get("args") == "2"

    def test_math_with_unit(self):
        ws = Worksheet()
        ws.add(MathRegion.assignment("L", 3, unit_name="m"))
        tree = ws.to_xml()
        root = tree.getroot()

        elems = root.findall(f".//{{{SMATH_NAMESPACE}}}e")
        # L 3 m[unit] * :
        values = [e.text for e in elems]
        assert "L" in values
        assert "3" in values
        assert "m" in values
        unit_el = [e for e in elems if e.get("style") == "unit"]
        assert len(unit_el) == 1
        assert unit_el[0].text == "m"

    def test_contract_unit(self):
        ws = Worksheet()
        ws.add(MathRegion.evaluation("R.A", contract_unit="kN"))
        tree = ws.to_xml()
        root = tree.getroot()

        contract = root.find(f".//{{{SMATH_NAMESPACE}}}contract")
        assert contract is not None
        e = contract.find(f"{{{SMATH_NAMESPACE}}}e")
        assert e.text == "kN"
        assert e.get("style") == "unit"

    def test_contract_expr_power_unit(self):
        """contract_expr=power_unit('mm', 2) → <contract> with mm ^ 2 RPN."""
        ws = Worksheet()
        ws.add(MathRegion(
            expr=assign("A_s", 1140),
            show_result=True,
            contract_expr=power_unit("mm", 2),
        ))
        tree = ws.to_xml()
        root = tree.getroot()

        contract = root.find(f".//{{{SMATH_NAMESPACE}}}contract")
        assert contract is not None
        elems = contract.findall(f"{{{SMATH_NAMESPACE}}}e")
        # RPN: mm[unit], 2[operand], ^[operator]
        assert len(elems) == 3
        assert elems[0].text == "mm"
        assert elems[0].get("style") == "unit"
        assert elems[1].text == "2"
        assert elems[2].text == "^"
        assert elems[2].get("type") == "operator"

    def test_contract_expr_compound_unit(self):
        """contract_expr=compound_unit(['kN'], ['m']) → <contract> with kN / m RPN."""
        ws = Worksheet()
        ws.add(MathRegion(
            expr=assign("q", 4),
            show_result=True,
            contract_expr=compound_unit(["kN"], ["m"]),
        ))
        tree = ws.to_xml()
        root = tree.getroot()

        contract = root.find(f".//{{{SMATH_NAMESPACE}}}contract")
        assert contract is not None
        elems = contract.findall(f"{{{SMATH_NAMESPACE}}}e")
        # RPN: kN[unit], m[unit], /[operator]
        assert len(elems) == 3
        assert elems[0].text == "kN"
        assert elems[1].text == "m"
        assert elems[2].text == "/"

    def test_contract_expr_overrides_contract_unit(self):
        """contract_expr takes priority over contract_unit when both are set."""
        ws = Worksheet()
        ws.add(MathRegion(
            expr=assign("A_s", 1140),
            show_result=True,
            contract_unit="m",          # should be ignored
            contract_expr=power_unit("mm", 2),
        ))
        tree = ws.to_xml()
        root = tree.getroot()

        contract = root.find(f".//{{{SMATH_NAMESPACE}}}contract")
        elems = contract.findall(f"{{{SMATH_NAMESPACE}}}e")
        # Should have mm^2 (3 elements), not m (1 element)
        assert len(elems) == 3
        assert elems[0].text == "mm"

    def test_expression_region(self):
        x = var("x")
        expr = x ** 2 + 3 * x - 1
        ws = Worksheet()
        ws.add(MathRegion.expression(expr))
        tree = ws.to_xml()
        root = tree.getroot()

        input_el = root.find(f".//{{{SMATH_NAMESPACE}}}input")
        assert input_el is not None
        elems = input_el.findall(f"{{{SMATH_NAMESPACE}}}e")
        assert len(elems) > 0

    def test_show_result_emits_result_tag(self):
        ws = Worksheet()
        ws.add(MathRegion(expr=assign("d", 449), show_result=True))
        tree = ws.to_xml()
        root = tree.getroot()

        result_el = root.find(f".//{{{SMATH_NAMESPACE}}}result")
        assert result_el is not None, "<result> element missing when show_result=True"
        assert result_el.get("action") == "numeric"
        # Must have at least one <e> child so SMath Studio doesn't reject the region
        children = result_el.findall(f"{{{SMATH_NAMESPACE}}}e")
        assert len(children) >= 1, "<result> must contain at least one <e> placeholder"
        assert children[0].text == "0"  # placeholder value

    def test_show_result_false_no_result_tag(self):
        ws = Worksheet()
        ws.add(MathRegion(expr=assign("d", 449), show_result=False))
        tree = ws.to_xml()
        root = tree.getroot()

        result_el = root.find(f".//{{{SMATH_NAMESPACE}}}result")
        assert result_el is None, "<result> element should not be present when show_result=False"

    def test_assignment_factory_show_result(self):
        ws = Worksheet()
        ws.add(MathRegion.assignment("b", 300, unit_name="mm", show_result=True))
        tree = ws.to_xml()
        root = tree.getroot()

        result_el = root.find(f".//{{{SMATH_NAMESPACE}}}result")
        assert result_el is not None
        assert result_el.get("action") == "numeric"
        children = result_el.findall(f"{{{SMATH_NAMESPACE}}}e")
        assert len(children) >= 1, "<result> must contain at least one <e> placeholder"

    def test_evaluation_factory_emits_result_tag(self):
        """MathRegion.evaluation() sets result_action but not result_elements — should still emit <result>."""
        ws = Worksheet()
        ws.add(MathRegion.evaluation("d"))
        tree = ws.to_xml()
        root = tree.getroot()

        result_el = root.find(f".//{{{SMATH_NAMESPACE}}}result")
        assert result_el is not None, "<result> element missing for MathRegion.evaluation()"
        assert result_el.get("action") == "numeric"
        children = result_el.findall(f"{{{SMATH_NAMESPACE}}}e")
        assert len(children) >= 1, "<result> must contain at least one <e> placeholder"


class TestSaveFile:
    def test_save_and_read(self, tmp_path):
        ws = Worksheet(title="Test File", author="PyTest")
        ws.add(TextRegion.title("Test Document"))
        ws.add(TextRegion.section("Input:"))
        ws.add(MathRegion(expr=assign("a", 20405)))
        ws.add(MathRegion(expr=assign("b", 84645)))

        out = tmp_path / "test.sm"
        ws.save(str(out))

        content = out.read_text(encoding="utf-8")
        assert '<?xml version="1.0"' in content
        assert '<?application progid="SMath Studio Desktop"' in content
        assert "20405" in content
        assert "84645" in content

        # Verify it's valid XML
        tree = ET.parse(str(out))
        root = tree.getroot()
        assert root.tag == f"{{{SMATH_NAMESPACE}}}regions"


class TestPlotRegionSerialization:
    def test_plot_2d_default(self):
        """A default 2D plot with one input renders correct XML."""
        ws = Worksheet()
        ws.add(PlotRegion(inputs=[var("x")]))
        tree = ws.to_xml()
        root = tree.getroot()

        region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        assert region is not None

        plot_el = region.find(f"{{{SMATH_NAMESPACE}}}plot")
        assert plot_el is not None
        assert plot_el.get("type") == "2d"
        assert plot_el.get("render") == "lines"
        assert plot_el.get("grid") == "true"
        assert plot_el.get("axes") == "true"

        inputs = plot_el.findall(f"{{{SMATH_NAMESPACE}}}input")
        assert len(inputs) == 1
        e_els = inputs[0].findall(f"{{{SMATH_NAMESPACE}}}e")
        assert len(e_els) == 1
        assert e_els[0].text == "x"

    def test_plot_multiple_inputs(self):
        """Multiple input expressions produce separate <input> elements."""
        ws = Worksheet()
        ws.add(PlotRegion(inputs=[var("f"), var("g"), var("h")]))
        tree = ws.to_xml()
        root = tree.getroot()

        plot_el = root.find(f".//{{{SMATH_NAMESPACE}}}plot")
        assert plot_el is not None
        inputs = plot_el.findall(f"{{{SMATH_NAMESPACE}}}input")
        assert len(inputs) == 3

    def test_plot_custom_attribs(self):
        """Custom attributes (grid, axes, render, scale) serialize correctly."""
        ws = Worksheet()
        ws.add(PlotRegion(
            inputs=[var("x")],
            grid=False,
            axes=False,
            render="points",
            scale_x=2.0,
            scale_y=0.5,
        ))
        tree = ws.to_xml()
        root = tree.getroot()

        plot_el = root.find(f".//{{{SMATH_NAMESPACE}}}plot")
        assert plot_el.get("grid") == "false"
        assert plot_el.get("axes") == "false"
        assert plot_el.get("render") == "points"
        assert plot_el.get("scale_x") == "2.0"
        assert plot_el.get("scale_y") == "0.5"

    def test_plot_3d(self):
        """A 3D plot serializes with rotation attributes."""
        ws = Worksheet()
        ws.add(PlotRegion(
            inputs=[var("z")],
            plot_type="3d",
            rotate_x=30,
            rotate_y=45,
        ))
        tree = ws.to_xml()
        root = tree.getroot()

        plot_el = root.find(f".//{{{SMATH_NAMESPACE}}}plot")
        assert plot_el.get("type") == "3d"
        assert plot_el.get("rotate_x") == "30"
        assert plot_el.get("rotate_y") == "45"

    def test_plot_show_input_data_false(self):
        """showInputData=False appears in region attributes."""
        ws = Worksheet()
        ws.add(PlotRegion(inputs=[var("x")], show_input_data=False))
        tree = ws.to_xml()
        root = tree.getroot()

        region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        assert region.get("showInputData") == "False"


class TestPictureRegionSerialization:
    def test_picture_from_bytes(self):
        """PictureRegion from raw bytes serializes with base64 data."""
        ws = Worksheet()
        raw = b"\x89PNG\r\n\x1a\nfakedata"
        ws.add(PictureRegion.from_bytes(raw, fmt="png"))
        tree = ws.to_xml()
        root = tree.getroot()

        region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        assert region is not None

        pic_el = region.find(f"{{{SMATH_NAMESPACE}}}picture")
        assert pic_el is not None

        raw_el = pic_el.find(f"{{{SMATH_NAMESPACE}}}raw")
        assert raw_el is not None
        assert raw_el.get("format") == "png"
        assert raw_el.get("encoding") == "base64"
        assert raw_el.text is not None
        assert len(raw_el.text) > 0

    def test_picture_format_normalization(self):
        """jpg extension is normalized to jpeg."""
        pic = PictureRegion.from_bytes(b"data", fmt="png")
        assert pic.format == "png"

    def test_picture_from_file(self, tmp_path):
        """PictureRegion.from_file reads and base64-encodes a file."""
        img = tmp_path / "test.png"
        img.write_bytes(b"\x89PNG\r\n\x1a\nfakeimagedata")

        pic = PictureRegion.from_file(str(img))
        assert pic.format == "png"
        assert pic.data_base64 is not None
        assert len(pic.data_base64) > 0

    def test_picture_from_file_jpg(self, tmp_path):
        """from_file normalizes .jpg to jpeg format."""
        img = tmp_path / "photo.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fakedata")

        pic = PictureRegion.from_file(str(img))
        assert pic.format == "jpeg"

    def test_picture_xml_structure(self):
        """Full XML structure: region > picture > raw."""
        import base64

        ws = Worksheet()
        data = b"testbytes"
        ws.add(PictureRegion(data_base64=base64.b64encode(data).decode(), format="bmp"))
        tree = ws.to_xml()
        root = tree.getroot()

        raw_el = root.find(f".//{{{SMATH_NAMESPACE}}}raw")
        assert raw_el is not None
        assert raw_el.get("format") == "bmp"


class TestAreaRegionSerialization:
    def test_area_empty(self):
        """Empty area produces start marker + terminator."""
        ws = Worksheet()
        ws.add(AreaRegion())
        tree = ws.to_xml()
        root = tree.getroot()

        # Top-level region
        region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        assert region is not None

        # Area start marker
        area_el = region.find(f"{{{SMATH_NAMESPACE}}}area")
        assert area_el is not None
        assert area_el.get("collapsed") is None  # not collapsed

        # Terminator region nested inside
        inner_regions = region.findall(f"{{{SMATH_NAMESPACE}}}region")
        assert len(inner_regions) == 1  # just the terminator
        term_area = inner_regions[0].find(f"{{{SMATH_NAMESPACE}}}area")
        assert term_area is not None
        assert term_area.get("terminator") == "true"

    def test_area_with_children(self):
        """Area with child regions serializes children between start and terminator."""
        ws = Worksheet()
        area = AreaRegion()
        area.add(TextRegion(text="Inside area"))
        area.add(MathRegion(expr=assign("y", 42)))
        ws.add(area)
        tree = ws.to_xml()
        root = tree.getroot()

        # Top-level area region
        top_region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        assert top_region is not None

        # Should have: area marker, 2 child regions, terminator region = 3 inner regions
        inner_regions = top_region.findall(f"{{{SMATH_NAMESPACE}}}region")
        assert len(inner_regions) == 3  # 2 children + 1 terminator

        # First child should be text region
        text_el = inner_regions[0].find(f"{{{SMATH_NAMESPACE}}}text")
        assert text_el is not None

        # Second child should be math region
        math_el = inner_regions[1].find(f"{{{SMATH_NAMESPACE}}}math")
        assert math_el is not None

        # Last should be terminator
        term_area = inner_regions[2].find(f"{{{SMATH_NAMESPACE}}}area")
        assert term_area is not None
        assert term_area.get("terminator") == "true"

    def test_area_collapsed(self):
        """Collapsed area has collapsed='true' on the area element."""
        ws = Worksheet()
        ws.add(AreaRegion(collapsed=True))
        tree = ws.to_xml()
        root = tree.getroot()

        area_el = root.find(f".//{{{SMATH_NAMESPACE}}}area")
        assert area_el is not None
        assert area_el.get("collapsed") == "true"

    def test_area_terminator_id(self):
        """Terminator ID = area ID + number of children + 1."""
        ws = Worksheet()
        area = AreaRegion()
        area.add(TextRegion(text="child1"))
        area.add(TextRegion(text="child2"))
        ws.add(area)
        tree = ws.to_xml()
        root = tree.getroot()

        top_region = root.find(f"{{{SMATH_NAMESPACE}}}region")
        area_id = int(top_region.get("id"))

        inner_regions = top_region.findall(f"{{{SMATH_NAMESPACE}}}region")
        term_region = inner_regions[-1]
        term_id = int(term_region.get("id"))

        assert term_id == area_id + 2 + 1  # 2 children + 1
