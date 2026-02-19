"""Example: Engineering beam calculation with units."""

from smathpy import Worksheet, TextRegion, MathRegion, var, assign, evaluate
from smathpy.expression import sum_, func_assign, call
from smathpy.units import with_unit, value_with_compound_unit


def main():
    ws = Worksheet(title="Viga de Hormigón Armado ACI318-19", author="smathpy")

    # ── Title ──
    ws.add(TextRegion.title("Viga de Hormigón Armado ACI318-19"))

    # ── Input Data ──
    ws.add(TextRegion.section("Datos de entrada:"))

    ws.add(MathRegion.assignment("b", 300, unit_name="mm")) # width of the beam
    ws.add(MathRegion.assignment("h", 300, unit_name="mm")) # height of the beam
    ws.add(MathRegion.assignment("rec", 50, unit_name="mm")) # concrete cover
    ws.add(MathRegion.assignment("f_c", 25, unit_name="MPa")) # concrete compressive strength
    ws.add(MathRegion.assignment("f_y", 420, unit_name="MPa")) # yield strength of the reinforcement





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
