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
    ws.add(MathRegion(expr=assign("q_i", value_with_compound_unit(4, ["kN"], ["m"]))))

    # ── Calculations ──
    ws.add(TextRegion.section("Calculations:"))

    for i in range(10):
        ws.add(MathRegion.assignment(f"x_{i}", i**2, unit_name="m"))

    ws.save("output/prueba.sm")
    print("✓ Saved output/prueba.sm")


if __name__ == "__main__":
    main()
