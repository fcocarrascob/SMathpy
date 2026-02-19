"""Tests for document creation and XML serialization."""

import xml.etree.ElementTree as ET

from smathpy import Worksheet, TextRegion, MathRegion, assign, var, num, evaluate
from smathpy.constants import SMATH_NAMESPACE


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
