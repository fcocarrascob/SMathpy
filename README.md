# smathpy

Python API for programmatic generation of [SMath Studio](https://smath.com/) worksheet (`.sm`) files.

Generate parametric engineering calculations, numerical method worksheets, and mathematical documents entirely from Python code — no GUI needed.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from smathpy import Worksheet, TextRegion, MathRegion, var, assign, evaluate

ws = Worksheet(title="My Calculation", author="Engineer")

ws.add(TextRegion.title("Simple Calculation"))
ws.add(TextRegion.section("Input data:"))
ws.add(MathRegion.assignment("L", 3, unit_name="m"))
ws.add(MathRegion.assignment("q", 4, unit_name="kN"))

ws.add(TextRegion.section("Calculation:"))
ws.add(MathRegion(expr=assign("R", var("q") * var("L") / 2)))

ws.add(TextRegion.section("Result:"))
ws.add(MathRegion.evaluation("R", contract_unit="kN"))

ws.save("calculation.sm")
```

The generated `.sm` file opens directly in SMath Studio.

## Features

### Expressions with Operator Overloading

```python
from smathpy import var, num, assign, func_assign

x = var("x")
expr = x ** 2 + 3 * x - 1       # builds RPN automatically

# Function definitions
f_def = func_assign("f", ["x"], x ** 2)

# Assignments
a = assign("h", (var("b") - var("a")) / var("n"))
```

### Units

```python
from smathpy import MathRegion
from smathpy.units import with_unit, value_with_compound_unit

# Simple unit: L := 3 * m
MathRegion.assignment("L", 3, unit_name="m")

# Compound unit: q := 4 * kN/m
from smathpy import assign
assign("q", value_with_compound_unit(4, ["kN"], ["m"]))
```

### Matrices

```python
from smathpy.expression import mat, el, det, transpose

# 2×2 matrix
m = mat([[1, 2], [3, 4]])

# Element access
e = el("A", "i", "j")

# Operations
d = det("A")
t = transpose("A")
```

### Control Structures

```python
from smathpy.expression import for_range, while_loop, if_, line, range_, sum_

# For loop with range
body = assign("s", var("s") + var("i"))
loop = for_range("i", range_(1, "n"), body)

# While loop
w = while_loop(var("x") > 0, assign("x", var("x") - 1))

# Conditional
c = if_(var("x") > 0, var("a"), var("b"))

# Summation
s = sum_(var("k") ** 2, "k", 1, "n")
```

### Built-in Functions

```python
from smathpy.expression import (
    abs_, sin, cos, tan, sqrt, exp, ln,    # math
    diff, diff_n, integral,                 # calculus
    concat, num2str,                        # string
    mod, sign, eval_,                       # misc
)
```

### Region Types

| Type | Class | Description |
|------|-------|-------------|
| Text | `TextRegion` | Formatted text, multilingual support |
| Math | `MathRegion` | Mathematical expressions and calculations |
| Plot | `PlotRegion` | 2D charts and graphs |
| Picture | `PictureRegion` | Embedded images (PNG, JPEG) |
| Area | `AreaRegion` | Collapsible sections |

### Text Region Shortcuts

```python
TextRegion.title("Title")          # Bold, blue, 12pt
TextRegion.section("Input data:")  # Bordered, gray background
TextRegion(texts={"eng": "Hello", "rus": "Привет"})  # Multilingual
```

## Examples

See the `examples/` directory:

- `generate_gcd.py` — Euclidean GCD algorithm (while/if/line)
- `generate_beam.py` — Engineering beam with units
- `generate_simpson.py` — Simpson's rule numerical integration

Run any example:

```bash
python examples/generate_gcd.py
```

## Project Structure

```
smathpy/
├── __init__.py           # Public API
├── document.py           # Worksheet class & XML serialization
├── settings.py           # Document settings, metadata, page model
├── constants.py          # XML namespace, assemblies, built-in functions
├── expression/
│   ├── builder.py        # Expr class with operator overloading
│   ├── elements.py       # RPN element types (operand, operator, function)
│   ├── functions.py      # Built-in math function wrappers
│   ├── matrix.py         # Matrix construction & operations
│   └── control.py        # Control structures (for, while, if, line)
├── regions/
│   ├── base.py           # Base Region class
│   ├── text_region.py    # TextRegion
│   ├── math_region.py    # MathRegion
│   ├── plot_region.py    # PlotRegion
│   ├── picture_region.py # PictureRegion
│   └── area_region.py    # AreaRegion (collapsible sections)
└── units/
    └── __init__.py       # Unit helpers & common unit constants
```

## Target Format

Generates SMath Studio v0.98 format (compatible with v0.96+ readers). Output is standard XML with the `http://smath.info/schemas/worksheet/1.0` namespace.

## License

MIT
