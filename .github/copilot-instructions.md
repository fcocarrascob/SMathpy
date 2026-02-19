# Copilot Instructions — smathpy

## Project Overview

**smathpy** is a Python API that programmatically generates SMath Studio worksheet (`.sm`) XML files. It does **not** evaluate expressions — it builds Reverse Polish Notation (RPN) element lists that serialize into SMath-compatible XML.

## Architecture

```
smathpy/
├── document.py        # Worksheet: top-level container, auto-layout, XML serialization
├── settings.py        # Settings, Metadata, PageModel, Assembly dataclasses
├── constants.py       # XML namespace, colors, fonts, BUILTIN_FUNCTIONS catalog, paper sizes
├── expression/
│   ├── builder.py     # Expr class (immutable RPN list), operator overloading, var/num/assign/call helpers
│   ├── elements.py    # Element dataclass — the atomic <e> tag (operand/operator/function/bracket)
│   ├── functions.py   # Thin wrappers: abs_, sin, diff, integral, etc. → call(name, *args)
│   ├── control.py     # Control flow: for_range, while_loop, if_, line, sum_, product_
│   └── matrix.py      # mat(), el(), det(), transpose(), etc.
├── regions/
│   ├── base.py        # Region base dataclass (position, color, font)
│   ├── math_region.py # MathRegion: holds an Expr + result/contract/description
│   ├── text_region.py # TextRegion: multilingual text with .title() / .section() class methods
│   ├── plot_region.py # PlotRegion
│   ├── picture_region.py
│   └── area_region.py # AreaRegion: collapsible container for child regions
└── units/
    └── __init__.py    # with_unit(), compound_unit(), value_with_compound_unit(), power_unit(), unit constants
```

### Key Concept: RPN Expression Model

All math is represented as `Expr` — an ordered list of `Element` objects in RPN order. Operators and functions go **after** their operands. Python operator overloading on `Expr` builds the RPN automatically:

```python
x = var("x")
expr = x ** 2 + 3 * x - 1  # Expr([x, 2, ^, 3, x, *, +, 1, -])
```

Elements have a `type` (`"operand"`, `"operator"`, `"function"`, `"bracket"`), a `value`, and optional `args` count. Functions with names in `BUILTIN_FUNCTIONS` (see `constants.py`) get `preserve=True`.

### Worksheet Pipeline

`Worksheet.add(region)` → auto-layout (assigns `top` position) → `to_xml()` assigns sequential IDs → `_build_region()` serializes each region type → `save()` writes XML with SMath processing instructions.

`Worksheet.add_spacing(pixels)` inserts extra vertical gap between regions by bumping `_next_top` without adding a region. Use it to create visual separation between calculation blocks.

## Conventions

- **Dataclasses everywhere**: `Region`, `MathRegion`, `TextRegion`, `Settings`, `Element` are all `@dataclass`.
- **Class methods as factories**: `TextRegion.title()`, `TextRegion.section()`, `MathRegion.assignment()`, `MathRegion.evaluation()` are the idiomatic constructors.
- **Trailing underscores** for Python keyword clashes: `abs_`, `if_`, `sum_`, `round_`, `max_`, `min_`, `eval_`, `product_`.
- **`_coerce()` pattern**: Internal helper in `builder.py` converts `int`/`float`/`str` to `Expr` — all public APIs accept `Union[Expr, int, float, str]`.
- **Units via `@` operator**: `num(5) @ "m"` attaches a unit using `__matmul__`.
- **`power_unit(unit, exp)`**: builds a unit-raised-to-power expression (e.g. `power_unit('mm', 2)` for mm²) — preferred over `compound_unit(['mm','mm'], [])` for readability when used as `contract_expr`.
- **Comparison operators return `Expr`**, not `bool`. Use `.eq()` and `.neq()` for equality (can't safely override `__eq__`/`__ne__`).

## Development Workflow

```bash
pip install -e ".[dev]"     # editable install with pytest, black, ruff
pytest                       # run all tests
pytest tests/test_golden.py  # golden-file structural tests
python examples/api_reference.py  # generates output/api_reference.sm
```

## Testing Patterns

- Tests assert on RPN element lists (`expr.elements[i].value`, `.type`, `.args`) — not string output.
- `test_golden.py` recreates known `.sm` files (e.g., EuclideanGCD) and verifies XML region count and structure with `xml.etree.ElementTree`.
- `test_document.py` tests full serialization: XML attributes, namespace correctness, metadata, region ordering.
- Tests import from `smathpy.expression` for internal types and from `smathpy` for public API.

## Adding New Features

- **New math function**: Add a wrapper in `functions.py` using `call(name, *args)`, export from `expression/__init__.py` and `smathpy/__init__.py`. If the function is a SMath built-in, add its name to `BUILTIN_FUNCTIONS` in `constants.py`.
- **New region type**: Subclass `Region` in `regions/`, add serialization in `document.py`'s `_build_region()` method, export from `regions/__init__.py`.
- **New control structure**: Add to `control.py` following the `for_range`/`while_loop` pattern — build RPN elements manually, end with `function(name, arg_count)`.

## XML Format Notes

- Namespace: `http://smath.info/schemas/worksheet/1.0` — all elements are namespaced.
- Target version: SMath Studio Desktop `0.98.6606.22069`.
- `.sm` files start with two processing instructions (`<?xml ...?>` and `<?application ...?>`), then `<regions>` root.
