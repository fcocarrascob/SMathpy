"""Example: Engineering beam calculation with units."""

from smathpy import Worksheet, TextRegion, MathRegion, var, assign, evaluate
from smathpy.expression import sum_, func_assign, call
from smathpy.units import with_unit, value_with_compound_unit


def main():
    ws = Worksheet(title="Simple Beam Calculation", author="smathpy")

    # ── Title ──
    ws.add(TextRegion.title("Simple Beam Calculation"))

    # ── Input Data ──
    ws.add(TextRegion.section("Input data:"))

    # L := 3 * m
    ws.add(MathRegion.assignment("L", 3, unit_name="m"))

    # q := 4 * kN/m  (distributed load)
    ws.add(MathRegion(expr=assign("q", value_with_compound_unit(4, ["kN"], ["m"]))))

    # ── Calculations ──
    ws.add(TextRegion.section("Calculations:"))

    # R.A = q*L/2  (support reaction)
    q, L = var("q"), var("L")
    ws.add(MathRegion(expr=assign("R.A", q * L / 2)))

    # M.max = q*L^2/8  (maximum moment)
    ws.add(MathRegion(expr=assign("M.max", q * L ** 2 / 8)))

    # ── Results ──
    ws.add(TextRegion.section("Results:"))
    ws.add(MathRegion.evaluation("R.A", contract_unit="kN"))
    ws.add(MathRegion.evaluation("M.max", contract_unit="kN"))

    ws.save("output/beam_generated.sm")
    print("✓ Saved output/beam_generated.sm")


if __name__ == "__main__":
    main()
