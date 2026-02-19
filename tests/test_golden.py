"""Golden-file test: recreate EuclideanGCD.sm and compare structure."""

import xml.etree.ElementTree as ET

from smathpy import Worksheet, TextRegion, MathRegion, var, assign, evaluate
from smathpy.expression import (
    abs_, mod, if_, while_loop, line,
)
from smathpy.constants import SMATH_NAMESPACE


def test_euclidean_gcd_structure():
    """Recreate EuclideanGCD.sm and verify the XML structure matches."""
    ws = Worksheet(title="Euclidean algorithm (calculating the GCD)", author="Test")

    # Title
    ws.add(TextRegion.title("Euclidean algorithm\n(calculating the GCD)"))

    # Input data section
    ws.add(TextRegion.section("Input data:"))

    # a := 20405
    ws.add(MathRegion(expr=assign("a", 20405)))

    # b := 84645
    ws.add(MathRegion(expr=assign("b", 84645)))

    # Calculation section
    ws.add(TextRegion.section("Calculation:"))

    # x := abs(a)
    ws.add(MathRegion(expr=assign("x", abs_("a"))))

    # y := abs(b)
    ws.add(MathRegion(expr=assign("y", abs_("b"))))

    # The while loop with if inside, then GCD := x+y, wrapped in line
    x = var("x")
    y = var("y")

    condition = x.neq(0).and_(y.neq(0))

    true_branch = assign("x", mod("x", "y"))
    false_branch = assign("y", mod("y", "x"))

    if_expr = if_(x > y, true_branch, false_branch)
    while_expr = while_loop(condition, if_expr)
    gcd_assign = assign("GCD", x + y)

    body = line(while_expr, gcd_assign)
    ws.add(MathRegion(expr=body))

    # Result section
    ws.add(TextRegion.section("Result:"))

    # GCD evaluation
    ws.add(MathRegion(expr=evaluate("GCD")))

    # Control section
    ws.add(TextRegion.section("Control:"))

    # a/GCD and b/GCD
    ws.add(MathRegion(expr=var("a") / var("GCD")))
    ws.add(MathRegion(expr=var("b") / var("GCD")))

    # Verify XML structure
    tree = ws.to_xml()
    root = tree.getroot()

    # Count regions (4 text sections + 7 math + 2 math for a/GCD, b/GCD = 13)
    regions = root.findall(f"{{{SMATH_NAMESPACE}}}region")
    assert len(regions) == 13

    # Verify first math region has correct RPN
    math_regions = [
        r for r in regions
        if r.find(f"{{{SMATH_NAMESPACE}}}math") is not None
    ]
    assert len(math_regions) >= 2

    # Check a := 20405
    first_math = math_regions[0]
    elems = first_math.findall(f".//{{{SMATH_NAMESPACE}}}e")
    texts = [e.text for e in elems]
    assert texts == ["a", "20405", ":"]

    # Verify the while/if block is present
    all_elems = root.findall(f".//{{{SMATH_NAMESPACE}}}e")
    func_names = [e.text for e in all_elems if e.get("type") == "function"]
    assert "while" in func_names
    assert "if" in func_names
    assert "mod" in func_names
    assert "abs" in func_names
    assert "line" in func_names


def test_save_euclidean_gcd(tmp_path):
    """Save a generated EuclideanGCD file and verify it's valid XML."""
    ws = Worksheet(title="Euclidean GCD", author="smathpy")
    ws.add(TextRegion.title("Euclidean algorithm"))
    ws.add(MathRegion(expr=assign("a", 20405)))
    ws.add(MathRegion(expr=assign("b", 84645)))

    path = tmp_path / "EuclideanGCD_gen.sm"
    ws.save(str(path))

    # Verify valid XML
    tree = ET.parse(str(path))
    root = tree.getroot()
    assert root.tag == f"{{{SMATH_NAMESPACE}}}regions"

    # Verify processing instructions are present in raw text
    content = path.read_text(encoding="utf-8")
    assert '<?application progid="SMath Studio Desktop"' in content
