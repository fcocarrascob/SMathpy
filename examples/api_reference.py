#!/usr/bin/env python3
"""
SMathPy — API Reference Example
================================

This script demonstrates the majority of the smathpy API features.
Open the generated .sm file in SMath Studio to see the results.

Sections covered:
  1. Worksheet & Settings
  2. Text Regions (title, section, multilingual, custom colours)
  3. Expression Builders (var, num, const, string, placeholder)
  4. Operator Overloading (+, -, *, /, **, comparisons, logical, factorial)
  5. Assignments & Definitions (assign, define, func_assign, evaluate)
  6. Built-in Math Functions (abs, sqrt, trig, exp/ln/log, ceil/floor, round, mod, sign)
  7. Calculus (diff, diff_n, integral)
  8. String Functions (concat, num2str)
  9. Matrix Operations (mat, el, rows, cols, det, transpose, tr, identity, augment, stack, csort, polyroots)
  10. Control Structures (line, range_, for_range, for_loop, while_loop, if_, sum_, product_)
  11. Units (with_unit, compound_unit, value_with_compound_unit, @-operator, unit constants)
  12. MathRegion Helpers (assignment, evaluation, expression, description, contract_unit)
  13. Plot Region
  14. Picture Region (synthetic)
  15. Area Region (collapsible)
  16. Save to file

Run:
    python examples/api_reference.py
"""

from pathlib import Path

# ── Core ────────────────────────────────────────────────────────────────────
from smathpy import (
    Worksheet,
    TextRegion,
    MathRegion,
    PlotRegion,
    PictureRegion,
    AreaRegion,
    Settings,
    Metadata,
    PageModel,
)

# ── Expression builders ────────────────────────────────────────────────────
from smathpy import (
    var, num, const, string, unit, placeholder,
    assign, define, func_assign, evaluate, call,
)

# ── Math functions ──────────────────────────────────────────────────────────
from smathpy.expression import (
    # Basic math
    abs_, sign, sqrt, exp, ln, log, ceil, floor, round_, mod, max_, min_,
    # Trigonometric
    sin, cos, tan, asin, acos, atan,
    # Calculus
    diff, diff_n, integral,
    # String
    concat, num2str,
    # Evaluation helper
    eval_,
)

# ── Matrix operations ──────────────────────────────────────────────────────
from smathpy.expression import (
    mat, el, rows, cols, row, col,
    transpose, det, tr, identity,
    augment, stack, csort, polyroots, cinterp,
)

# ── Control structures ─────────────────────────────────────────────────────
from smathpy.expression import (
    line, range_, for_range, for_loop, while_loop, if_, sum_, product_,
)

# ── Units ───────────────────────────────────────────────────────────────────
from smathpy.units import (
    with_unit, compound_unit, value_with_compound_unit,
    # Length
    m, cm, mm, km, inch, ft,
    # Force
    N, kN, MN,
    # Mass
    kg, g,
    # Time
    s,
    # Pressure / Stress
    Pa, kPa, MPa, GPa,
    # Temperature
    K,
    # Angle
    rad, deg,
)


# ═══════════════════════════════════════════════════════════════════════════
#  1. WORKSHEET & SETTINGS
# ═══════════════════════════════════════════════════════════════════════════

ws = Worksheet(
    settings=Settings(
        metadata=[Metadata(
            title="SMathPy API Reference",
            author="SMathPy",
            description="Comprehensive demo of every API feature",
        )],
        precision=4,
        page_model=PageModel(),  # defaults to A4
    )
)


# ═══════════════════════════════════════════════════════════════════════════
#  2. TEXT REGIONS
# ═══════════════════════════════════════════════════════════════════════════

# Title (bold, blue, larger font)
ws.add(TextRegion.title("SMathPy — API Reference Manual"))

# Section divider (bordered, grey background)
ws.add(TextRegion.section("2. Text Regions"))

# Plain text
ws.add(TextRegion(text="This is a plain text region."))

# Bold text with custom colour
ws.add(TextRegion(text="Bold red text", bold=True, color="#cc0000"))

# Multilingual text (SMath can display the user's language)
ws.add(TextRegion(
    texts={"eng": "Hello, World!", "spa": "¡Hola, Mundo!", "rus": "Привет, мир!"},
    bold=True,
))


# ═══════════════════════════════════════════════════════════════════════════
#  3. EXPRESSION BUILDERS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("3. Expression Builders"))

# var — a named variable
x = var("x")
y = var("y")
z = var("z")
n = var("n")
i = var("i")
k = var("k")
t = var("t")
a = var("a")
b = var("b")

# num — a numeric literal
five = num(5)

# const — a named constant (π, e)
pi = const("π")
e  = const("e")

# string — a string literal
greeting = string("Hello")

# placeholder — a blank operand (·)
ph = placeholder()

# Show a simple expression built with var and num
ws.add(MathRegion.expression(assign("x", num(42))))
ws.add(MathRegion.expression(assign("greeting", greeting)))


# ═══════════════════════════════════════════════════════════════════════════
#  4. OPERATOR OVERLOADING
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("4. Operator Overloading"))

# Arithmetic: +  -  *  /  **
expr_arith = x**2 + num(3) * x - num(1)
ws.add(MathRegion.expression(assign("f.arith", expr_arith)))

# Division and power
expr_frac = (x + y) / (x - y)
ws.add(MathRegion.expression(assign("f.frac", expr_frac)))

# Unary negation
ws.add(MathRegion.expression(assign("neg.x", -x)))

# Reverse operators (int/float on the left)
ws.add(MathRegion.expression(assign("rev", 2 + x)))
ws.add(MathRegion.expression(assign("rev2", 10 - x)))
ws.add(MathRegion.expression(assign("rev3", 3 * x)))

# Comparisons  >  <  >=  <=
ws.add(MathRegion.expression(assign("cmp.gt", x > y)))
ws.add(MathRegion.expression(assign("cmp.le", x <= num(10))))

# Not-equal and equality (can't override __eq__/__ne__ safely)
ws.add(MathRegion.expression(assign("cmp.neq", x.neq(y))))
ws.add(MathRegion.expression(assign("cmp.eq", x.eq(y))))

# Logical AND
ws.add(MathRegion.expression(assign("logic", (x > 0).and_(x < 10))))

# Factorial
ws.add(MathRegion.expression(assign("fact5", num(5).factorial())))

# Grouping (bracket hint for display)
ws.add(MathRegion.expression(assign("grp", (x + y).grouped() * z)))


# ═══════════════════════════════════════════════════════════════════════════
#  5. ASSIGNMENTS & DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("5. Assignments & Definitions"))

# assign (name := value)
ws.add(MathRegion.expression(assign("L", num(10))))

# define (name ≡ value)  — for symbolic equivalences
ws.add(MathRegion.expression(define("σ.max", var("F") / var("A"))))

# func_assign — define a user function  f(x) := body
ws.add(MathRegion.expression(
    func_assign("f", ["x"], x**2 + 2*x + 1)
))

# Multi-parameter function  g(x,y) := x² + y²
ws.add(MathRegion.expression(
    func_assign("g", ["x", "y"], x**2 + y**2)
))

# evaluate — push a variable for evaluation
ws.add(MathRegion.expression(evaluate("L")))

# call — invoke a function
ws.add(MathRegion.expression(assign("result.f", call("f", num(3)))))
ws.add(MathRegion.expression(assign("result.g", call("g", num(1), num(2)))))


# ═══════════════════════════════════════════════════════════════════════════
#  6. BUILT-IN MATH FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("6. Built-in Math Functions"))

ws.add(MathRegion.expression(assign("v.abs",   abs_(-num(7)))))
ws.add(MathRegion.expression(assign("v.sign",  sign(-num(3)))))
ws.add(MathRegion.expression(assign("v.sqrt",  sqrt(num(144)))))
ws.add(MathRegion.expression(assign("v.exp",   exp(num(1)))))
ws.add(MathRegion.expression(assign("v.ln",    ln(e))))
ws.add(MathRegion.expression(assign("v.log",   log(num(100)))))       # log₁₀
ws.add(MathRegion.expression(assign("v.ceil",  ceil(num(3.2)))))
ws.add(MathRegion.expression(assign("v.floor", floor(num(3.8)))))
ws.add(MathRegion.expression(assign("v.round", round_(num(3.456)))))
ws.add(MathRegion.expression(assign("v.mod",   mod(num(17), num(5)))))
ws.add(MathRegion.expression(assign("v.max",   call("max", num(3), num(7)))))
ws.add(MathRegion.expression(assign("v.min",   call("min", num(3), num(7)))))


# ═══════════════════════════════════════════════════════════════════════════
#  6b. TRIGONOMETRIC FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("6b. Trigonometric Functions"))

ws.add(MathRegion.expression(assign("v.sin",  sin(pi / 2))))
ws.add(MathRegion.expression(assign("v.cos",  cos(pi))))
ws.add(MathRegion.expression(assign("v.tan",  tan(pi / 4))))
ws.add(MathRegion.expression(assign("v.asin", asin(num(1)))))
ws.add(MathRegion.expression(assign("v.acos", acos(num(0)))))
ws.add(MathRegion.expression(assign("v.atan", atan(num(1)))))


# ═══════════════════════════════════════════════════════════════════════════
#  7. CALCULUS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("7. Calculus"))

# First derivative: d/dx (x³)
ws.add(MathRegion.expression(assign("deriv1", diff(x**3, x))))

# n-th derivative: d²/dx² (x⁴)
ws.add(MathRegion.expression(assign("deriv2", diff_n(x**4, x, num(2)))))

# Definite integral: ∫₀¹ x² dx
ws.add(MathRegion.expression(assign("integ", integral(x**2, x, num(0), num(1)))))


# ═══════════════════════════════════════════════════════════════════════════
#  8. STRING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("8. String Functions"))

ws.add(MathRegion.expression(
    assign("s.concat", concat(string("Hello"), string(", World!")))
))
ws.add(MathRegion.expression(
    assign("s.num2str", num2str(num(3.14)))
))


# ═══════════════════════════════════════════════════════════════════════════
#  9. MATRIX OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("9. Matrix Operations"))

# mat — construct a matrix from a 2D list
A_val = mat([[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]])
ws.add(MathRegion.expression(assign("A", A_val)))

B_val = mat([[1, 0],
             [0, 1]])
ws.add(MathRegion.expression(assign("B", B_val)))

# Vector (column)
v_val = mat([[10], [20], [30]])
ws.add(MathRegion.expression(assign("V", v_val)))

# el — element access  A[i,j]  (1-based in SMath)
ws.add(MathRegion.expression(assign("a12", el(var("A"), num(1), num(2)))))

# 1D element access (vector)
ws.add(MathRegion.expression(assign("v2", el(var("V"), num(2)))))

# rows, cols
ws.add(MathRegion.expression(assign("nr", rows(var("A")))))
ws.add(MathRegion.expression(assign("nc", cols(var("A")))))

# row, col extraction
ws.add(MathRegion.expression(assign("r1", row(var("A"), num(1)))))
ws.add(MathRegion.expression(assign("c2", col(var("A"), num(2)))))

# det — determinant
ws.add(MathRegion.expression(assign("d", det(var("B")))))

# transpose
ws.add(MathRegion.expression(assign("At", transpose(var("A")))))

# tr — trace
ws.add(MathRegion.expression(assign("trace.A", tr(var("A")))))

# identity
ws.add(MathRegion.expression(assign("I3", identity(num(3)))))

# augment — horizontal concatenation
ws.add(MathRegion.expression(assign("AB", augment(var("B"), var("B")))))

# stack — vertical concatenation
ws.add(MathRegion.expression(assign("BB", stack(var("B"), var("B")))))

# csort — sort by column
ws.add(MathRegion.expression(assign("As", csort(var("A"), num(1)))))

# polyroots — roots of a polynomial (coefficients vector)
coeffs = mat([[1], [-3], [2]])   # x² - 3x + 2 → roots 1, 2
ws.add(MathRegion.expression(assign("p.coeffs", coeffs)))
ws.add(MathRegion.expression(assign("p.roots", polyroots(var("p.coeffs")))))

# cinterp — cubic interpolation
xs = mat([[0], [1], [2], [3]])
ys = mat([[0], [1], [8], [27]])
ws.add(MathRegion.expression(assign("xs", xs)))
ws.add(MathRegion.expression(assign("ys", ys)))
ws.add(MathRegion.expression(
    assign("interp", cinterp(var("xs"), var("ys"), num(1.5)))
))


# ═══════════════════════════════════════════════════════════════════════════
# 10. CONTROL STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("10. Control Structures"))

# line — group multiple statements into a single block
ws.add(MathRegion.expression(
    assign("blk", line(
        assign("a", num(1)),
        assign("b", num(2)),
        a + b,
    ))
))

# range_ — create a range  1..10
ws.add(MathRegion.expression(assign("rng", range_(num(1), num(10)))))

# range with step  0, 0.5 .. 5
ws.add(MathRegion.expression(assign("rng.s", range_(num(0), num(0.5), num(5)))))

# for_range — for(var, range, body)  (3-arg form)
ws.add(MathRegion.expression(
    for_range("i", range_(num(1), num(5)), i**2)
))

# for_loop — C-style for (var, start, condition, increment, body)
ws.add(MathRegion.expression(
    for_loop(
        "k",                           # variable name
        num(0),                        # start value
        k < num(10),                   # condition
        k + num(1),                    # increment
        k**2,                          # body
    )
))

# while_loop
ws.add(MathRegion.expression(
    while_loop(
        n > num(0),                    # condition
        assign("n", n - num(1)),       # body
    )
))

# if_ — conditional expression  if(cond, then, else)
ws.add(MathRegion.expression(
    assign("cond", if_(x > 0, string("positive"), string("non-positive")))
))

# sum_ — Σ  sum_(body, var, start, end)
ws.add(MathRegion.expression(
    assign("sigma", sum_(i**2, i, num(1), num(10)))
))

# product_ — Π  product_(body, var, start, end)
ws.add(MathRegion.expression(
    assign("pi.prod", product_(i, i, num(1), num(5)))
))


# ═══════════════════════════════════════════════════════════════════════════
# 11. UNITS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("11. Units"))

# @-operator: attach a unit to a numeric value
ws.add(MathRegion.expression(assign("length", num(5) @ "m")))
ws.add(MathRegion.expression(assign("force", num(10) @ "kN")))

# with_unit helper (same as @ but function-style)
ws.add(MathRegion.expression(assign("mass", with_unit(num(75), "kg"))))

# compound_unit — e.g. kN/m  (numerator list, denominator list)
ws.add(MathRegion.expression(
    assign("pressure", value_with_compound_unit(num(200), ["kN"], ["m"]))
))

# value_with_compound_unit — compact helper
ws.add(MathRegion.expression(
    assign("stress", value_with_compound_unit(num(15), ["MPa"]))
))

# Pre-built unit constants as Expr  (m, cm, kN, kg, …)
ws.add(MathRegion.expression(assign("u.m",  m)))
ws.add(MathRegion.expression(assign("u.cm", cm)))
ws.add(MathRegion.expression(assign("u.kN", kN)))
ws.add(MathRegion.expression(assign("u.Pa", Pa)))
ws.add(MathRegion.expression(assign("u.deg", deg)))

# MathRegion.assignment shortcut with unit_name
ws.add(MathRegion.assignment("L.beam", 12, unit_name="m"))
ws.add(MathRegion.assignment("q", 5, unit_name="kN"))

# MathRegion.evaluation with contract_unit (unit conversion on output)
ws.add(MathRegion.evaluation("L.beam", contract_unit="cm"))


# ═══════════════════════════════════════════════════════════════════════════
# 12. MATHREGION HELPERS
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("12. MathRegion Helpers"))

# MathRegion.expression — raw expression
ws.add(MathRegion.expression(x + y))

# MathRegion.assignment — shorthand for a := value
ws.add(MathRegion.assignment("height", 3.5, unit_name="m"))

# MathRegion.evaluation — evaluate a variable
ws.add(MathRegion.evaluation("height"))

# description — an annotation shown next to the math region
ws.add(MathRegion.expression(
    assign("E", num(200000) @ "MPa"),
    description="Young's Modulus of Steel",
))

# decimal_places — control numeric precision per region
ws.add(MathRegion(
    expr=assign("pi.val", pi),
    decimal_places=8,
    description="Pi with 8 decimal places",
))


# ═══════════════════════════════════════════════════════════════════════════
# 13. PLOT REGION
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("13. Plot Region"))

# Define a variable for the plotter
ws.add(MathRegion.expression(
    func_assign("plotter", ["x"], sin(x))
))

# PlotRegion — 2D plot
ws.add(PlotRegion(
    inputs=[var("plotter")],
    plot_type="2d",
    render="lines",
    grid=True,
    axes=True,
    width=400,
    height=300,
))


# ═══════════════════════════════════════════════════════════════════════════
# 14. PICTURE REGION (synthetic 1×1 PNG)
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("14. Picture Region"))

# PictureRegion.from_bytes — embed raw image data
# Create a minimal 1×1 red PNG (67 bytes) for demonstration
import struct, zlib
def _make_tiny_png() -> bytes:
    """Return a valid 1×1 red PNG as bytes."""
    sig = b'\x89PNG\r\n\x1a\n'
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xFFFFFFFF
    ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    # IDAT
    raw = zlib.compress(b'\x00\xff\x00\x00')  # filter-none + red pixel
    idat_crc = zlib.crc32(b'IDAT' + raw) & 0xFFFFFFFF
    idat = struct.pack('>I', len(raw)) + b'IDAT' + raw + struct.pack('>I', idat_crc)
    # IEND
    iend_crc = zlib.crc32(b'IEND') & 0xFFFFFFFF
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    return sig + ihdr + idat + iend

ws.add(PictureRegion.from_bytes(_make_tiny_png(), fmt="png", width=50, height=50))

# Note: use PictureRegion.from_file("path/to/image.png") for real images.


# ═══════════════════════════════════════════════════════════════════════════
# 15. AREA REGION (collapsible section)
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("15. Area Region (Collapsible)"))

area = AreaRegion(collapsed=False)
area.add(TextRegion(text="This content is inside a collapsible area."))
area.add(MathRegion.assignment("inside.a", 100))
area.add(MathRegion.assignment("inside.b", 200))
area.add(MathRegion.expression(assign("inside.sum", var("inside.a") + var("inside.b"))))
ws.add(area)


# ═══════════════════════════════════════════════════════════════════════════
# 16. EVAL & MISC
# ═══════════════════════════════════════════════════════════════════════════

ws.add(TextRegion.section("16. Misc: eval, call, grouped"))

# eval_ — programmatic evaluation of an expression
ws.add(MathRegion.expression(assign("ev", eval_(x + y))))

# call — generic function call
ws.add(MathRegion.expression(assign("c.abs", call("abs", num(-99)))))
ws.add(MathRegion.expression(assign("c.max", call("max", num(3), num(7)))))

# grouped — explicit bracketing
ws.add(MathRegion.expression(
    assign("g.expr", (a + b).grouped() * (a - b).grouped())
))


# ═══════════════════════════════════════════════════════════════════════════
# 17. SAVE
# ═══════════════════════════════════════════════════════════════════════════

output_dir = Path(__file__).resolve().parent.parent / "output"
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "api_reference.sm"

ws.save(str(output_path))
print(f"✔ Saved: {output_path}")
print(f"  Regions: {len(ws.regions)}")
