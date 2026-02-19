"""Example: Recreate the EuclideanGCD.sm example using smathpy."""

from smathpy import Worksheet, TextRegion, MathRegion, var, assign, evaluate
from smathpy.expression import abs_, mod, if_, while_loop, line


def main():
    ws = Worksheet(title="Euclidean algorithm (calculating the GCD)", author="smathpy")

    # ── Title ──
    ws.add(TextRegion.title("Euclidean algorithm\n(calculating the GCD)"))

    # ── Input data ──
    ws.add(TextRegion.section("Input data:"))
    ws.add(MathRegion(expr=assign("a", 20405)))
    ws.add(MathRegion(expr=assign("b", 84645)))

    # ── Calculation ──
    ws.add(TextRegion.section("Calculation:"))
    ws.add(MathRegion(expr=assign("x", abs_("a"))))
    ws.add(MathRegion(expr=assign("y", abs_("b"))))

    # Build the algorithm: while/if loop + GCD assignment in a line block
    x, y = var("x"), var("y")

    condition = x.neq(0).and_(y.neq(0))
    if_expr = if_(
        x > y,
        assign("x", mod("x", "y")),
        assign("y", mod("y", "x")),
    )
    while_expr = while_loop(condition, if_expr)
    gcd_assign = assign("GCD", x + y)

    ws.add(MathRegion(expr=line(while_expr, gcd_assign)))

    # ── Result ──
    ws.add(TextRegion.section("Result:"))
    ws.add(MathRegion(expr=evaluate("GCD")))

    # ── Control ──
    ws.add(TextRegion.section("Control:"))
    ws.add(MathRegion(expr=var("a") / var("GCD")))
    ws.add(MathRegion(expr=var("b") / var("GCD")))

    ws.save("output/EuclideanGCD_generated.sm")
    print("✓ Saved output/EuclideanGCD_generated.sm")


if __name__ == "__main__":
    main()
