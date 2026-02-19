# SMath Python API for Template Generation

**Branch:** `feature/smath-python-api`
**Description:** Build a Python API to programmatically generate SMath (.sm) template files from code

## Goal
Create a comprehensive Python library that enables programmatic generation of SMath Studio documents. The API will parse the XML structure of .sm files and provide intuitive Python classes for building mathematical worksheets, expressions, and engineering calculations. This eliminates the need for manual XML manipulation and provides a pythonic way to create SMath templates.

## Implementation Steps

### Step 1: Project Foundation and Core Document Structure
**Files:** 
- `pyproject.toml`
- `smathpy/__init__.py`
- `smathpy/document.py`
- `smathpy/settings.py`
- `smathpy/constants.py`
- `tests/test_document.py`
- `tests/conftest.py`
- `README.md`
- `.gitignore`
- `LICENSE`

**What:** Establish the project structure and implement the core `SMathDocument` class that handles document creation, settings configuration (identity, metadata, calculation precision, page model), and XML serialization. This includes namespace handling, version support, and basic file I/O. Set up pytest configuration and project packaging.

**Testing:** 
- Create a minimal SMath document with settings
- Verify XML structure matches SMath schema
- Test file save/load operations
- Validate generated .sm file opens correctly in SMath Studio
- Set up golden file comparison framework

---

### Step 2: Region System and Text Regions
**Files:**
- `smathpy/regions/__init__.py`
- `smathpy/regions/base.py`
- `smathpy/regions/text_region.py`
- `smathpy/regions/region_builder.py`
- `tests/test_regions.py`
- `tests/test_text_regions.py`

**What:** Implement the region positioning system and text region functionality. Create base `Region` class with positioning (left, top, width, height), styling (colors, borders, fonts), and multilingual text support. Build `TextRegion` class for adding formatted text content in multiple languages.

**Testing:**
- Add text regions at specific positions
- Test multilingual text (English, Spanish/Russian)
- Verify region styling (colors, borders, fonts)
- Generate document with multiple text regions and verify in SMath

---

### Step 3: Expression Builder with RPN Support
**Files:**
- `smathpy/expression/__init__.py`
- `smathpy/expression/builder.py`
- `smathpy/expression/elements.py`
- `smathpy/expression/operators.py`
- `tests/test_expression_builder.py`

**What:** Implement the `MathExpression` builder class that handles Reverse Polish Notation (RPN) for mathematical expressions. Support basic operands (variables, numbers), operators (+, -, *, /, ^, :), and expression stacking. Provide fluent API for building expressions programmatically.

**Testing:**
- Build simple assignments: `x := 5`
- Build arithmetic expressions: `a + b * c`
- Verify RPN ordering is correct
- Test operator precedence handling
- Validate expressions in generated SMath documents

---

### Step 4: Math Regions and Basic Calculations
**Files:**
- `smathpy/regions/math_region.py`
- `smathpy/expression/functions.py`
- `tests/test_math_regions.py`
- `examples/basic_calculation.py`

**What:** Implement `MathRegion` class that integrates with expression builder. Add support for input/result sections, descriptions, and basic mathematical functions (sin, cos, sqrt, abs, etc.). Enable numeric and symbolic computation modes.

**Testing:**
- Create math regions with variable assignments
- Add regions with basic calculations
- Test function calls (trig, logarithmic, etc.)
- Generate example document similar to examples/GravitationAcceleration.sm
- Verify calculations execute correctly in SMath

---

### Step 5: Units System and Physical Quantities
**Files:**
- `smathpy/units/__init__.py`
- `smathpy/units/unit_handler.py`
- `smathpy/units/common_units.py`
- `tests/test_units.py`
- `examples/engineering_calculation.py`

**What:** Implement unit support for physical quantities. Create `UnitHandler` class that attaches units to operands using the `style="unit"` attribute. Provide common unit definitions (m, kg, s, N, Pa, etc.) and unit conversion helpers. Integrate with expression builder.

**Testing:**
- Assign values with units: `length := 5 * m`
- Perform unit-aware calculations
- Test unit consistency checking with optional validation flag
- Generate engineering document similar to examples/Beam.sm
- Verify units display correctly in SMath

---

### Step 6: Matrix Operations and Advanced Functions
**Files:**
- `smathpy/expression/matrix.py`
- `smathpy/expression/advanced_functions.py`
- `tests/test_matrices.py`
- `examples/matrix_calculation.py`

**What:** Add matrix construction (`mat` function), element access (`el` function), and matrix operations (rows, cols, sum, transpose, determinant). Implement differentiation (`diff`) and advanced mathematical functions. Support nested matrix definitions and indexing.

**Testing:**
- Create matrices programmatically
- Access matrix elements
- Perform matrix operations (transpose, determinant, etc.)
- Test symbolic differentiation
- Generate document similar to examples/Jacobian.sm or examples/Hessian.sm

---

### Step 7: Control Structures and Iteration
**Files:**
- `smathpy/expression/control.py`
- `smathpy/expression/loops.py`
- `tests/test_control_structures.py`
- `examples/numerical_method.py`

**What:** Implement programming constructs: `range`, `for`, `while`, `if` conditionals. Enable iterative algorithms and numerical methods. Support nested loops and complex control flow for algorithms like Newton-Raphson, Runge-Kutta, Simpson integration.

**Testing:**
- Create range-based loops
- Implement while loop with conditions
- Build conditional expressions
- Generate numerical method document (examples/Newton.sm, examples/RungeKutta5.sm)
- Verify iterative calculations execute correctly

---

### Step 8: Plot and Picture Regions
**Files:**
- `smathpy/regions/plot_region.py`
- `smathpy/regions/picture_region.py`
- `smathpy/utils/image_encoder.py`
- `tests/test_plot_regions.py`
- `tests/test_picture_regions.py`
- `examples/plot_example.py`

**What:** Implement `PlotRegion` for embedding charts and graphs, and `PictureRegion` for embedding images. Support base64 encoding of images (PNG, JPEG), plot configuration, and positioning. Provide helpers for common plot types and image import utilities.

**Testing:**
- Embed images in documents
- Test base64 encoding/decoding
- Create plot regions with configuration
- Generate document with embedded graphics
- Verify images/plots display in SMath Studio

---

### Step 9: High-Level Templates and Documentation
**Files:**
- `smathpy/templates/__init__.py`
- `smathpy/templates/standard_layout.py`
- `smathpy/templates/numerical_methods.py`
- `smathpy/templates/engineering.py`
- `docs/api_reference.md`
- `docs/getting_started.md`
- `docs/examples.md`
- `examples/README.md`
- `examples/complete_workflow.py`

**What:** Create high-level template classes for common document patterns (Title → Input → Calculation → Result workflow). Provide templates for numerical methods, engineering calculations, and mathematical analysis. Write comprehensive API documentation with real-world examples.

**Testing:**
- Use templates to quickly generate common document types
- Verify templates match standard SMath patterns
- Test all example files run successfully
- Validate documentation accuracy
- Generate complex multi-section documents

---

## Design Decisions

Based on your feedback, the following design decisions have been made:

### ✅ Unit System Behavior
**Decision:** Optional validation flag (best of both worlds)

The API will include a configurable validation mode:
```python
# Strict mode - validates unit consistency
doc = SMathDocument(unit_validation=True)

# Permissive mode - passes units through
doc = SMathDocument(unit_validation=False)
```

### ✅ Python Version Support
**Decision:** Python 3.8+ (modern features, type hints)

This provides:
- Modern type hints for better IDE support
- Standard library improvements
- Wide compatibility (Python 3.8 released Oct 2019)

### ✅ Expression API Style
**Decision:** Both styles supported

The API will provide multiple ways to build expressions:
```python
# Style 1: Fluent/chained API (explicit, clear)
expr = MathExpression()
expr.operand('x').operand(5).operator('+', 2)

# Style 2: Operator overloading (pythonic, intuitive)
from smathpy.expression import var
x = var('x')
expr = x + 5

# Style 3: String parsing (convenient for simple cases)
expr = parse_expression("x + 5")
```

### ✅ Additional Features
**Decision:** Include Plot and Picture regions in initial version

This enables complete document generation with:
- Embedded images (base64-encoded)
- Charts and graphs
- Visual documentation

### ℹ️ Legacy Schema Support
**Decision:** Modern format only (0.98+)

The initial version will target the modern schema. Legacy support can be added in a future update if needed.

### ✅ Testing Strategy
**Decision:** Unit tests + golden file comparison

The testing approach will include:
- Unit tests for individual components
- Golden file comparison against known-good .sm reference files
- No SMath Studio installation required for CI/CD

### ✅ Package Name
**Decision:** `smathpy`

Simple, clear, and follows Python naming conventions.

---

## Open Questions

*No open questions remaining. Plan is ready for implementation.*

---
### Package Name
What should the Python package be named on PyPI?

**Suggestions:**
- `smathpy` (simple, clear)
- `smath-studio` (descriptive)
- `pysmath` (Python convention)
- Custom name?

---

## Technical Notes

- **Package Name:** `smathpy`
- **Primary Language:** Python 3.8+
- **Primary Dependency:** `xml.etree.ElementTree` (Python standard library)
- **Optional Dependencies:** `lxml` (for advanced validation), `pytest` (testing), `black` (formatting), `Pillow` (image handling)
- **Testing Strategy:** Unit tests + golden file comparison against reference .sm files
- **Complexity:** Medium-High due to RPN expression handling and nested XML structures
- **Expression Styles:** Fluent API, operator overloading, and string parsing all supported
- **Unit Validation:** Optional validation flag for unit consistency checks
- **Estimated Timeline:** 10-15 days for full implementation with tests and documentation (9 steps)

## Success Criteria

✅ Generate valid .sm files that open in SMath Studio without errors
✅ Support all common mathematical operations and functions
✅ Provide intuitive, pythonic API
✅ Include comprehensive test coverage (>80%)
✅ Deliver clear documentation with real examples
✅ Enable rapid template creation for common engineering calculations
