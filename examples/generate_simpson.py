"""Example: Simpson's rule numerical integration using smathpy."""

from smathpy import Worksheet, TextRegion, MathRegion, var, assign, evaluate, func_assign
from smathpy.expression import sum_, range_, for_range, call


def main():
    ws = Worksheet(title="Numeric integration (Simpson's rule)", author="smathpy")

    # ── Title ──
    ws.add(TextRegion.title("Numeric integration method\n(Simpson's rule)"))

    # ── Input data ──
    ws.add(TextRegion.section("Input data:"))

    # f(x) := x^2
    x = var("x")
    ws.add(MathRegion(expr=func_assign("f", ["x"], x ** 2),
                       description="integrand"))

    # bounds and accuracy
    ws.add(MathRegion(expr=assign("a", 1), description="inferior limit"))
    ws.add(MathRegion(expr=assign("b", 5), description="superior limit"))
    ws.add(MathRegion(expr=assign("n", 20), description="accuracy"))

    # ── Calculation ──
    ws.add(TextRegion.section("Calculation:"))

    # h := (b-a)/n
    b, a, n = var("b"), var("a"), var("n")
    ws.add(MathRegion(expr=assign("h", (b - a) / n)))

    # Simpson formula using sum
    k = var("k")
    h_var = var("h")
    summation = sum_(
        call("f", a + h_var * (2 * k - 1)),
        "k", 1, n
    )
    ws.add(MathRegion(expr=assign("S", summation)))

    # ── Result ──
    ws.add(TextRegion.section("Result:"))
    ws.add(MathRegion.evaluation("S"))

    ws.save("output/simpson_generated.sm")
    print("✓ Saved output/simpson_generated.sm")


if __name__ == "__main__":
    main()
