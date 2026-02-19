# SMath Studio .sm File Format — Comprehensive Research Report

> **Generated from:** Analysis of all 18 example `.sm` files in the `examples/` directory.
> **Purpose:** Inform implementation of the `smathpy` Python API.

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [SMath XML Format — Document Structure](#2-smath-xml-format--document-structure)
3. [XML Namespace & Schema Details](#3-xml-namespace--schema-details)
4. [Expression/RPN Analysis](#4-expressionrpn-analysis)
5. [Units System Analysis](#5-units-system-analysis)
6. [Matrix Analysis](#6-matrix-analysis)
7. [Region Positioning & Types](#7-region-positioning--types)
8. [Control Structures](#8-control-structures)
9. [Built-in Functions Catalog](#9-built-in-functions-catalog)
10. [Version Differences](#10-version-differences)
11. [Appendix: Per-File Inventory](#11-appendix-per-file-inventory)

---

## 1. Project Structure

### Current Workspace

```
SMathpy/
├── .github/
│   └── prompts/         # AI prompt templates
├── examples/            # 18 SMath Studio .sm example files
│   ├── Beam.sm
│   ├── ChordMethod.sm
│   ├── Dichotomy.sm
│   ├── EuclideanGCD.sm
│   ├── GravitationAcceleration.sm
│   ├── HermitePolynomials.sm
│   ├── Hessian.sm
│   ├── Jacobian.sm
│   ├── LaguerrePolynomials.sm
│   ├── LegendrePolynomials.sm
│   ├── MaclaurinSeries.sm
│   ├── Newton.sm
│   ├── PlanetaryGear.sm
│   ├── RomanNumerals.sm
│   ├── RungeKutta5.sm
│   ├── Simpson.sm
│   ├── SylvesterFormula.sm
│   └── Thomas.sm
└── plans/
    └── smath-python-api/
        └── plan.md
```

**No Python code exists yet.** No `pyproject.toml`, `.gitignore`, `README.md`, or `LICENSE`.

### File Size Distribution

| File | Lines | Complexity |
|------|------:|------------|
| Beam.sm | 1398 | Very High — units, matrices, collapsible areas, plot, string functions, nested loops |
| RungeKutta5.sm | 790 | High — adaptive-step ODE solver, complex `for`/`if`/`line` nesting |
| Thomas.sm | 680 | Medium — tridiagonal solver with `for`/`range`/`line` |
| SylvesterFormula.sm | ~370 | Medium — matrix ops, `product`/`sum`/`for` |
| Newton.sm | ~370 | Medium — v0.99 format, root-finding |
| PlanetaryGear.sm | ~400 | Medium — animation, collapsible areas, `eval`, `stack`, `sys` |
| GravitationAcceleration.sm | ~360 | Medium — picture, units, string operands, `description` |
| HermitePolynomials.sm | ~280 | Medium — diff, for, plot |
| LaguerrePolynomials.sm | ~280 | Medium — polyroots, plot |
| LegendrePolynomials.sm | ~280 | Medium — Rodrigues formula, plot |
| Jacobian.sm | ~250 | Medium — nested for, matrix construction |
| Hessian.sm | ~300 | Medium — nested for, det, symbolic |
| MaclaurinSeries.sm | ~220 | Low-Medium — sum, range, plot |
| ChordMethod.sm | ~200 | Low-Medium — while/if/line |
| Dichotomy.sm | ~200 | Low — while/if/line |
| RomanNumerals.sm | ~220 | Low-Medium — string ops, concat |
| Simpson.sm | ~200 | Low — sum, integration |
| EuclideanGCD.sm | ~130 | Low — while loop |

---

## 2. SMath XML Format — Document Structure

### 2.1 XML Prolog

Every `.sm` file begins with:

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<?application progid="SMath Studio Desktop" version="0.98.6606.22069"?>
```

The `<?application?>` processing instruction has two variants:

| Attribute | v0.96 | v0.98+ | v0.99+ |
|-----------|-------|--------|--------|
| `progid` | `"SMath Studio"` | `"SMath Studio Desktop"` | `"SMath Studio Desktop"` |
| `version` | `"0.96"` | `"0.98.6606.22069"` | `"0.99.6654.18973"` |

### 2.2 Root Element

**Two variants observed:**

#### Variant A — v0.96–0.98 (16 of 18 files)
```xml
<regions xmlns="http://smath.info/schemas/worksheet/1.0">
  <settings dpi="96">
    ...
  </settings>
  <region id="0" ...>...</region>
  <region id="1" ...>...</region>
  ...
</regions>
```

#### Variant B — v0.99+ (Newton.sm only)
```xml
<worksheet xmlns="http://smath.info/schemas/worksheet/1.0">
  <settings ppi="96">
    ...
  </settings>
  <regions type="content">
    <region id="0" ...>...</region>
    <region id="1" ...>...</region>
    ...
  </regions>
</worksheet>
```

**Key differences:**
- Root element: `<regions>` vs `<worksheet>`
- DPI attribute: `dpi="96"` vs `ppi="96"`
- Regions wrapper: none vs `<regions type="content">`
- Dependencies tag: `<dependences>` (typo) vs `<dependencies>` (correct)
- Functions: `preserve="true"` may be absent on some built-ins in v0.99

### 2.3 Settings Block

```xml
<settings dpi="96">
  <identity>
    <id>46f0669e-0077-4917-94b1-73396cc7f3ff</id>  <!-- UUID -->
    <revision>4</revision>
  </identity>
  <metadata lang="rus">
    <title>...</title>
    <author>...</author>
    <translator>...</translator>           <!-- optional -->
    <description>...</description>
    <company>SMath, http://smath.info/</company>  <!-- optional -->
    <keywords>...</keywords>
  </metadata>
  <metadata lang="eng">...</metadata>
  <metadata lang="ind">...</metadata>      <!-- Indonesian -->
  <metadata lang="gre">...</metadata>      <!-- Greek, in Newton.sm -->
  <calculation>
    <precision>4</precision>
    <exponentialThreshold>5</exponentialThreshold>
    <fractions>decimal</fractions>
  </calculation>
  <pageModel active="false" viewMode="2" printGrid="false" printAreas="true"
             simpleEqualsOnly="false" printBackgroundImages="true">
    <paper id="1" orientation="Portrait" width="850" height="1100" />
    <margins left="39" right="39" top="39" bottom="39" />
    <header alignment="Center" color="#a9a9a9">&amp;[DATE] &amp;[TIME] - &amp;[FILENAME]</header>
    <footer alignment="Center" color="#a9a9a9">&amp;[PAGENUM] / &amp;[COUNT]</footer>
    <backgrounds />
  </pageModel>
  <dependencies>
    <assembly name="SMath Studio Desktop" version="0.98.6606.22069"
              guid="a37cba83-b69c-4c71-9992-55ff666763bd" />
    <assembly name="Math Region" version="0.98.6606.22069"
              guid="02f1ab51-215b-466e-a74d-5d8b1cf85e8d" />
    <assembly name="Text Region" version="1.10.6606.22071"
              guid="485d28c5-349a-48b6-93be-12a35a1c1e39" />
    <assembly name="Special Functions" version="1.11.6606.22071"
              guid="2814e667-4e12-48b1-8d51-194e480eabc5" />
    <assembly name="Plot Region" version="1.9.6606.22072"
              guid="c451c2b5-798b-4f08-b9ec-b90963d1ddaa" />
  </dependencies>
</settings>
```

#### Settings Attributes Catalog

| Element | Attribute | Values | Notes |
|---------|-----------|--------|-------|
| `settings` | `dpi` / `ppi` | `96` | v0.96-0.98 uses `dpi`; v0.99 uses `ppi` |
| `metadata` | `lang` | `"rus"`, `"eng"`, `"ind"`, `"gre"` | ISO 639-2 language codes |
| `calculation/fractions` | — | `"decimal"` | Display mode for fractions |
| `pageModel` | `active` | `"false"`, `"true"` | Page model active state |
| `pageModel` | `viewMode` | `"2"` | Only seen in Beam.sm |
| `pageModel` | `printGrid` | `"false"` | Only seen in Beam.sm |
| `pageModel` | `printAreas` | `"true"`, `"false"` | |
| `pageModel` | `simpleEqualsOnly` | `"false"`, `"true"` | |
| `pageModel` | `printBackgroundImages` | `"true"` | |
| `paper` | `id` | `"1"` (Letter), `"9"` (A4) | Paper size ID |
| `paper` | `orientation` | `"Portrait"` | |
| `header`/`footer` | `alignment` | `"Center"` | |
| `header`/`footer` | `color` | `"#a9a9a9"` | |

#### Header/Footer Macros

- `&[DATE]` — Current date
- `&[TIME]` — Current time
- `&[FILENAME]` — File name
- `&[PAGENUM]` — Page number
- `&[COUNT]` — Total pages

#### Known Assembly GUIDs

| Name | GUID |
|------|------|
| SMath Studio (Desktop) | `a37cba83-b69c-4c71-9992-55ff666763bd` |
| Math Region | `02f1ab51-215b-466e-a74d-5d8b1cf85e8d` |
| Text Region | `485d28c5-349a-48b6-93be-12a35a1c1e39` |
| Special Functions | `2814e667-4e12-48b1-8d51-194e480eabc5` |
| Plot Region | `c451c2b5-798b-4f08-b9ec-b90963d1ddaa` |

---

## 3. XML Namespace & Schema Details

### Namespace

All `.sm` files use a single XML namespace:

```
http://smath.info/schemas/worksheet/1.0
```

This is declared on the root element (`<regions>` or `<worksheet>`).

### Schema Observations

There is no publicly documented XSD. All schema knowledge must be derived from the example files. Key observations:

1. **No DTD or XSD reference** in any file — the schema is implicit
2. **Namespace is consistent** across all versions (0.96 through 0.99)
3. **Element ordering** within `<settings>` is: `identity` → `metadata` (multiple) → `calculation` → `pageModel` → `dependences`/`dependencies`
4. **Region ordering** follows document top-to-bottom, left-to-right, but regions can be placed arbitrarily
5. **No CDATA sections** — all content uses standard XML text/entities
6. **XML entities used:** `&amp;` (in header/footer macros), `&lt;`/`&gt;` not observed

---

## 4. Expression/RPN Analysis

### 4.1 RPN Overview

All mathematical expressions are encoded in **Reverse Polish Notation (RPN)** using `<e>` (element) tags within `<input>`, `<result>`, or `<contract>` blocks.

SMath's RPN is a flat sequence of `<e>` elements. Each `<e>` has:
- `type` — One of: `operand`, `operator`, `function`, `bracket`
- `args` — (operators and functions only) Number of arguments consumed from the stack
- `style` — (operands only) Optional: `"unit"`, `"string"`
- `preserve` — (functions only) `"true"` for built-in functions

### 4.2 Element Types

#### Operands (`type="operand"`)

```xml
<e type="operand">x</e>           <!-- variable -->
<e type="operand">5</e>           <!-- integer -->
<e type="operand">3.14</e>        <!-- decimal -->
<e type="operand">0.1</e>         <!-- decimal with leading zero -->
<e type="operand">L.A</e>         <!-- dotted variable name -->
<e type="operand">arr.F</e>       <!-- dotted variable name -->
<e type="operand">δ</e>           <!-- Greek letter variable -->
<e type="operand">ε</e>           <!-- Greek letter variable -->
<e type="operand">β</e>           <!-- Greek letter variable -->
<e type="operand">γ</e>           <!-- Greek letter variable -->
<e type="operand">π</e>           <!-- Built-in constant pi -->
<e type="operand">.</e>           <!-- Placeholder dot (in display matrices) -->
<e type="operand">?</e>           <!-- Unknown placeholder -->
```

#### Operands with styles

```xml
<e type="operand" style="unit">m</e>      <!-- unit: meter -->
<e type="operand" style="unit">cm</e>     <!-- unit: centimeter -->
<e type="operand" style="unit">kN</e>     <!-- unit: kilonewton -->
<e type="operand" style="unit">dm</e>     <!-- unit: decimeter -->
<e type="operand" style="unit">km</e>     <!-- unit: kilometer -->
<e type="operand" style="string">RA</e>   <!-- string literal -->
<e type="operand" style="string">Green</e> <!-- string literal (color name) -->
```

#### Operators (`type="operator"`)

| Symbol | args | Description | Files |
|--------|------|-------------|-------|
| `:` | 2 | Assignment (`:=`) | All files |
| `≡` | 2 | Equation definition | ChordMethod, Dichotomy, RomanNumerals, Thomas, PlanetaryGear, RungeKutta5 |
| `+` | 2 | Addition | All files |
| `-` | 2 | Subtraction | Most files |
| `-` | 1 | Unary negation | Thomas, GravitationAcceleration, RungeKutta5 |
| `*` | 2 | Multiplication | Most files |
| `/` | 2 | Division | Most files |
| `^` | 2 | Exponentiation | Several files |
| `>` | 2 | Greater than | Dichotomy |
| `<` | 2 | Less than | |
| `≤` | 2 | Less than or equal | Dichotomy, RungeKutta5, Beam, SylvesterFormula |
| `≥` | 2 | Greater than or equal | |
| `≠` | 2 | Not equal | Dichotomy |
| `&` | 2 | Logical AND | Dichotomy, EuclideanGCD, RungeKutta5 |
| `!` | 1 | Factorial | HermitePolynomials, LegendrePolynomials |

**Critical insight:** The `:` operator (args=2) is the **assignment** operator, rendered as `:=` in SMath Studio. The `≡` operator is the **equation definition** (≡ sign in the UI), used for symbolic/display definitions.

#### Functions (`type="function"`)

Two categories:

1. **Built-in functions** — Have `preserve="true"`:
   ```xml
   <e type="function" preserve="true" args="1">abs</e>
   <e type="function" preserve="true" args="2">range</e>
   ```

2. **User-defined functions** — No `preserve` attribute:
   ```xml
   <e type="function" args="2">f</e>
   <e type="function" args="1">base.L</e>
   <e type="function" args="3">rect.Q</e>
   ```

**Note:** In Newton.sm (v0.99), some built-in functions lack `preserve="true"`. This is a version-specific difference.

#### Brackets (`type="bracket"`)

```xml
<e type="bracket">(</e>
```

Brackets serve as **grouping hints** for the renderer. They do not change RPN evaluation but affect visual display. They appear inline within the RPN stream to indicate where parentheses should be shown.

### 4.3 RPN Encoding Examples

#### Simple assignment: `x := 5`
```xml
<e type="operand">x</e>
<e type="operand">5</e>
<e type="operator" args="2">:</e>
```

#### Assignment with units: `L := 3 * m`
```xml
<e type="operand">L</e>
<e type="operand">3</e>
<e type="operand" style="unit">m</e>
<e type="operator" args="2">*</e>
<e type="operator" args="2">:</e>
```

#### Compound unit: `q := 4 * kN/m`
```xml
<e type="operand">q</e>
<e type="operand">4</e>
<e type="operand" style="unit">kN</e>
<e type="operand" style="unit">m</e>
<e type="operator" args="2">/</e>
<e type="operator" args="2">*</e>
<e type="operator" args="2">:</e>
```

#### Function call: `rows(A)`
```xml
<e type="operand">A</e>
<e type="function" preserve="true" args="1">rows</e>
```

#### Element access: `el(A, i, j)`
```xml
<e type="operand">A</e>
<e type="operand">i</e>
<e type="operand">j</e>
<e type="function" preserve="true" args="3">el</e>
```

#### Expression with bracket hint: `a + (b * c)`
```xml
<e type="operand">a</e>
<e type="operand">b</e>
<e type="operand">c</e>
<e type="operator" args="2">*</e>
<e type="bracket">(</e>
<e type="operator" args="2">+</e>
```

The bracket appears **after** the sub-expression it wraps, just before the operator that consumes it. This tells the renderer to display parentheses around `b*c`.

#### User function definition: `f(t, x) := f`
```xml
<e type="operand">t</e>
<e type="operand">x</e>
<e type="function" args="2">f</e>
<e type="operand">f</e>
<e type="operator" args="2">:</e>
```

### 4.4 Result Blocks

Math regions can contain `<result>` blocks:

```xml
<result action="numeric">
  <e type="operand">12.4533</e>
  <e type="operator" args="1">-</e>
</result>
```

```xml
<result action="symbolic">
  <e type="operand">4</e>
  <e type="operand">5</e>
  <e type="operator" args="2">/</e>
  ...
</result>
```

**Result actions:** `"numeric"` or `"symbolic"`

Results are also RPN-encoded. A cached result of `-12.4533` is stored as operand `12.4533` followed by unary negation.

### 4.5 Contract Blocks

The `<contract>` element specifies the **output unit** for display:

```xml
<math>
  <input>
    <e type="operand">R.A</e>
  </input>
  <contract>
    <e type="operand" style="unit">kN</e>
  </contract>
  <result action="numeric">
    <e type="operand">12.4533</e>
    <e type="operator" args="1">-</e>
  </result>
</math>
```

This means: "Display the value of `R.A` in units of `kN`." Found in Beam.sm for unit conversion on output.

### 4.6 Description Blocks

```xml
<math>
  <input>...</input>
  <description>
    <e type="operand" style="string">Gravitational acceleration at the surface</e>
  </description>
  <result action="numeric">...</result>
</math>
```

Found in GravitationAcceleration.sm. Provides descriptive text alongside a math result.

---

## 5. Units System Analysis

### 5.1 Unit Encoding

Units are operands with `style="unit"`:

```xml
<e type="operand" style="unit">m</e>
```

Units participate in RPN arithmetic like any other operand. They are multiplied/divided with numeric values:

```xml
<!-- 60 * cm -->
<e type="operand">60</e>
<e type="operand" style="unit">cm</e>
<e type="operator" args="2">*</e>
```

### 5.2 Compound Units

Compound units are built via arithmetic:

```xml
<!-- kN/m -->
<e type="operand" style="unit">kN</e>
<e type="operand" style="unit">m</e>
<e type="operator" args="2">/</e>

<!-- m³/(kg·s²) — from GravitationAcceleration.sm -->
<e type="operand" style="unit">m</e>
<e type="operand">3</e>
<e type="operator" args="2">^</e>
<e type="operand" style="unit">kg</e>
<e type="operator" args="2">/</e>
<e type="operand" style="unit">s</e>
<e type="operand">2</e>
<e type="operator" args="2">^</e>
<e type="operator" args="2">/</e>
```

### 5.3 Units Catalog from Examples

| Unit | Meaning | File |
|------|---------|------|
| `m` | meter | Beam, GravitationAcceleration |
| `cm` | centimeter | Beam |
| `dm` | decimeter | Beam (internal unit normalization) |
| `km` | kilometer | GravitationAcceleration |
| `kN` | kilonewton | Beam |
| `kg` | kilogram | GravitationAcceleration |
| `s` | second | GravitationAcceleration |

### 5.4 Unit Conversion on Output (`<contract>`)

The `<contract>` block in a `<math>` region specifies the desired output unit:

```xml
<contract>
  <e type="operand" style="unit">kN</e>
</contract>
```

This is a unique feature found in Beam.sm that allows results to be displayed in a specific unit, regardless of how they were computed.

---

## 6. Matrix Analysis

### 6.1 Matrix Construction — `mat` Function

Matrices are built using the `mat` function. The args count = `(num_data_elements + 2)`, where the last two elements pushed onto the stack are `rows` and `cols`.

```xml
<!-- 2×3 matrix with 6 data elements: mat has args=8 (6+2) -->
<e type="operand">10</e>      <!-- data[0,0] -->
<e type="operand">8</e>       <!-- data[0,1] -->
<e type="operand">17</e>      <!-- data[0,2] -->
<e type="operand">50</e>      <!-- data[1,0] -->
<e type="operand">1.1</e>     <!-- data[1,1] -->
<e type="operand">2.6</e>     <!-- data[1,2] -->
<e type="operand">2</e>       <!-- rows -->
<e type="operand">3</e>       <!-- cols -->
<e type="function" args="8">mat</e>
```

**Formula:** `args = rows × cols + 2`

**Note:** In some files (Beam.sm), `mat` has `preserve="true"`; in others it does not. Both forms appear to work:
- `<e type="function" args="8">mat</e>` (user-level context)
- `<e type="function" preserve="true" args="18">mat</e>` (Thomas.sm built-in context)

**Important:** Data elements can include units (Beam.sm) or complex sub-expressions. Each "data element" can be a full RPN sub-expression pushed onto the stack before `mat` consumes them.

### 6.2 Matrix with Units

From Beam.sm — a 2×3 matrix where cells have units:

```xml
<e type="operand">10</e>
<e type="operand" style="unit">kN</e>
<e type="operator" args="2">*</e>       <!-- 10*kN = one cell value -->
<e type="operand">8</e>
<e type="operand" style="unit">kN</e>
<e type="operator" args="2">*</e>       <!-- 8*kN -->
...
<e type="operand">2</e>
<e type="operand">3</e>
<e type="function" args="8">mat</e>     <!-- args = 2*3+2 = 8 -->
```

Each cell's entire RPN sub-expression counts as one logical element. The `args` count still reflects `rows*cols + 2`, not the total number of `<e>` tags.

### 6.3 Matrix Element Access — `el` Function

```xml
<!-- 1D access: el(vector, index) -->
<e type="operand">a</e>
<e type="operand">i</e>
<e type="function" preserve="true" args="2">el</e>

<!-- 2D access: el(matrix, row, col) -->
<e type="operand">A</e>
<e type="operand">i</e>
<e type="operand">j</e>
<e type="function" preserve="true" args="3">el</e>
```

### 6.4 Matrix Results in RPN

Matrix results are also stored in RPN:

```xml
<result action="numeric">
  <e type="operand">2</e>
  <e type="operand">2</e>
  <e type="operand">2</e>
  <e type="operand">2</e>
  <e type="operand">4</e>
  <e type="operand">1</e>
  <e type="function" preserve="true" args="6">mat</e>
</result>
```

### 6.5 Matrix Operations Catalog

| Function | args | Description | Files |
|----------|------|-------------|-------|
| `mat` | N+2 | Construct matrix (N = rows×cols) | Beam, Thomas, RungeKutta5, Jacobian, Hessian, GravitationAcceleration |
| `el` | 2 | Vector element access | Thomas, Simpson, RungeKutta5 |
| `el` | 3 | Matrix element access | Beam, Hessian, Jacobian, SylvesterFormula |
| `rows` | 1 | Number of rows | Thomas, GravitationAcceleration |
| `cols` | 1 | Number of columns | Beam, RungeKutta5, SylvesterFormula |
| `col` | 2 | Extract column | RungeKutta5, GravitationAcceleration |
| `row` | 2 | Extract row | RungeKutta5 |
| `transpose` | 1 | Matrix transpose | RungeKutta5 |
| `det` | 1 | Determinant | Hessian |
| `tr` | 1 | Matrix trace | SylvesterFormula |
| `identity` | 1 | Identity matrix | SylvesterFormula |
| `augment` | 2 | Horizontally append matrices | RungeKutta5 |
| `stack` | 2+ | Vertically stack matrices | Beam, RungeKutta5, PlanetaryGear, SylvesterFormula |
| `csort` | 2 | Sort by column | GravitationAcceleration |
| `polyroots` | 1 | Polynomial roots | LaguerrePolynomials, SylvesterFormula |
| `cinterp` | 3 | Cubic interpolation | RungeKutta5 |

---

## 7. Region Positioning & Types

### 7.1 Region Attributes

Every `<region>` has:

```xml
<region id="0" left="9" top="9" width="557" height="31"
        color="#0000ff" bgColor="#ffffff" fontSize="14">
```

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `id` | int | Unique region ID (sequential) | Yes |
| `left` | int | X position in pixels | Yes |
| `top` | int | Y position in pixels | Yes |
| `width` | int | Width in pixels | No (computed) |
| `height` | int | Height in pixels | No (computed) |
| `color` | hex | Text/foreground color | Yes |
| `bgColor` | hex | Background color | Yes |
| `fontSize` | int | Font size | No |
| `border` | `"true"` | Show border | No |
| `showInputData` | `"False"` | Hide input expression | No (Beam.sm plot) |

**Common colors:**
- `#000000` — Black (default text)
- `#0000ff` — Blue (titles)
- `#804040` — Brown (section headers)
- `#ffffff` — White (default background)
- `#ffff80` — Yellow (annotation labels)
- `#dddddd` — Gray (section divider backgrounds)
- `#80ff80` — Green (diagram background, Beam.sm)
- `#a9a9a9` — Dark gray (header/footer)

### 7.2 Region Types

#### Text Region

```xml
<region id="0" left="9" top="9" width="409" height="48"
        color="#0000ff" bgColor="#ffffff" fontSize="12">
  <text lang="rus">
    <p bold="true">Заголовок на русском</p>
  </text>
  <text lang="eng">
    <p bold="true">Title in English</p>
  </text>
  <text lang="ind">
    <p bold="true">Judul dalam Bahasa Indonesia</p>
  </text>
</region>
```

**Features:**
- Multiple `<text lang="...">` blocks for multilingual support
- `<p>` paragraph elements
- `bold="true"` attribute on `<p>`
- Multi-line text via separate text content (newlines preserved)
- `border="true"` on region for section dividers

#### Math Region

```xml
<region id="2" left="9" top="72" width="58" height="24"
        color="#000000" bgColor="#ffffff" fontSize="10">
  <math optimize="2">
    <input>
      <e type="operand">L</e>
      <e type="operand">3</e>
      <e type="operand" style="unit">m</e>
      <e type="operator" args="2">*</e>
      <e type="operator" args="2">:</e>
    </input>
  </math>
</region>
```

**Attributes on `<math>`:**
| Attribute | Values | Description |
|-----------|--------|-------------|
| `optimize` | `"2"` | Optimization level |
| `decimalPlaces` | int | Override decimal places |
| `significantDigitsMode` | `"true"` | Use significant digits |
| `trailingZeros` | `"true"` | Show trailing zeros |

**Sub-elements of `<math>`:**
| Element | Purpose | Required |
|---------|---------|----------|
| `<input>` | RPN expression (what user typed) | Yes |
| `<result action="...">` | Cached result (`numeric` or `symbolic`) | No |
| `<contract>` | Unit conversion for display | No |
| `<description>` | Descriptive string | No |

#### Plot Region

```xml
<region id="47" left="9" top="2430" width="556" height="233"
        color="#000000" bgColor="#80ff80" fontSize="10" showInputData="False">
  <plot grid="false" axes="false" type="2d" render="lines"
        scale_x="1.10535586945521" scale_y="1.10535586945521" scale_z="1.10535586945521"
        rotate_x="0" rotate_y="0" rotate_z="0"
        transpose_x="-243" transpose_y="-34" transpose_z="0">
    <input>
      <e type="operand">plotter</e>
    </input>
  </plot>
</region>
```

**Plot attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | string | `"2d"` |
| `render` | string | `"lines"` |
| `grid` | bool | Show grid lines |
| `axes` | bool | Show axes |
| `scale_x/y/z` | float | Zoom scale |
| `rotate_x/y/z` | int | Rotation angles |
| `transpose_x/y/z` | int | Pan offset |
| `animate` | string | `"t"` — animation variable (PlanetaryGear.sm) |

**Plot inputs:** RPN expressions for data series. Can include style operands:

```xml
<!-- From PlanetaryGear.sm: plot with color styling -->
<e type="operand" style="string">Blue</e>
```

Plots can have multiple `<input>` expressions for multiple series.

**Plot with animation** (PlanetaryGear.sm):
```xml
<plot animate="t" type="2d" render="lines" ...>
```

#### Picture Region

```xml
<region id="1" left="9" top="27" width="305" height="177"
        color="#000000" bgColor="#ffffff" fontSize="10">
  <picture>
    <raw format="png" encoding="base64">iVBORw0KGgo...base64data...</raw>
  </picture>
</region>
```

Only found in GravitationAcceleration.sm.

#### Area Region (Collapsible Sections)

```xml
<!-- Area start (can be collapsed) -->
<region id="15" top="351" color="#000000" bgColor="#ffffff">
  <area collapsed="true" />
  <!-- Child regions nested inside -->
  <region id="16" left="9" top="369" ...>...</region>
  <region id="17" left="9" top="396" ...>...</region>
  ...
  <!-- Area terminator -->
  <region id="45" top="2385" color="#000000" bgColor="#ffffff">
    <area terminator="true" />
  </region>
</region>
```

**Key behavior:**
- `<area collapsed="true" />` — section starts collapsed
- `<area />` (no attributes) — section starts expanded
- `<area terminator="true" />` — marks the end of the collapsible section
- Child regions are **nested inside** the parent `<region>`
- The area start region only has `id`, `top`, `color`, `bgColor` (no `left`, `width`, `height`)
- Found in: Beam.sm (2 collapsible sections), PlanetaryGear.sm

---

## 8. Control Structures

### 8.1 `for` Loop

```xml
<!-- for(i, start, condition, increment, body) -->
<e type="operand">i</e>              <!-- loop variable -->
<e type="operand">1</e>              <!-- start value -->
<e type="operator" args="2">:</e>    <!-- assignment: i := 1 -->
<e type="operand">i</e>
<e type="operand">n</e>
<e type="operator" args="2">≤</e>    <!-- condition: i ≤ n -->
<e type="operand">i</e>
<e type="operand">i</e>
<e type="operand">1</e>
<e type="operator" args="2">+</e>
<e type="operator" args="2">:</e>    <!-- increment: i := i + 1 -->
<!-- body expressions -->
<e type="operand">1</e>              <!-- line count in body -->
<e type="operand">1</e>              <!-- ??? (always 1) -->
<e type="function" preserve="true" args="N">line</e>  <!-- body block -->
<e type="function" preserve="true" args="4">for</e>
```

**`for` args = 4** always: `(init_assign, condition, increment, body)`

**Variant with `range`:**
```xml
<e type="operand">i</e>
<e type="operand">1</e>
<e type="operand">n</e>
<e type="function" preserve="true" args="2">range</e>
<!-- body -->
<e type="function" preserve="true" args="3">for</e>
```

`for` with `range` has **args=3**: `(variable, range, body)`.

### 8.2 `while` Loop

```xml
<!-- while(condition, body) -->
<e type="operand">i</e>
<e type="operand">n</e>
<e type="operator" args="2">≤</e>    <!-- condition -->
<!-- body expressions -->
<e type="operand">N</e>             
<e type="operand">1</e>
<e type="function" preserve="true" args="M">line</e>  <!-- body block -->
<e type="function" preserve="true" args="2">while</e>
```

`while` has **args=2**: `(condition, body)`

### 8.3 `if` Conditional

```xml
<!-- if(condition, true_body, false_body) -->
<e type="operand">x</e>
<e type="operand">0</e>
<e type="operator" args="2">></e>    <!-- condition -->
<!-- true branch -->
<!-- false branch -->
<e type="function" preserve="true" args="3">if</e>
```

`if` has **args=3**: `(condition, true_branch, false_branch)`

### 8.4 `line` Block

The `line` function groups multiple statements into a single body block:

```xml
<e type="function" preserve="true" args="5">line</e>
```

`line` args = `(num_statements + 2)`. The last two elements before `line` are typically `num_statements` and `1`.

**Pattern observed consistently:**
```xml
<!-- N statements here -->
<e type="operand">N</e>    <!-- number of statements -->
<e type="operand">1</e>    <!-- always 1 -->
<e type="function" preserve="true" args="N+2">line</e>
```

### 8.5 `range` Function

```xml
<!-- range(start, end) -->
<e type="operand">1</e>
<e type="operand">n</e>
<e type="function" preserve="true" args="2">range</e>

<!-- range(start, end, step) — descending range -->
<e type="operand">n</e>
<e type="operand">1</e>
<e type="operator" args="2">-</e>
<e type="operand">1</e>
<e type="operand">n</e>
<e type="operand">2</e>
<e type="operator" args="2">-</e>
<e type="function" preserve="true" args="3">range</e>
```

`range` has **args=2** (start, end) or **args=3** (start, end, step/direction).

### 8.6 `sum` and `product`

```xml
<!-- sum(expr, var, start, end) -->
<e type="operand">expr</e>
<e type="operand">k</e>
<e type="operand">1</e>
<e type="operand">n</e>
<e type="function" preserve="true" args="4">sum</e>

<!-- product(expr, var, start, end) -->
<e type="operand">expr</e>
<e type="operand">k</e>
<e type="operand">0</e>
<e type="operand">n</e>
<e type="function" preserve="true" args="4">product</e>
```

Both have **args=4**: `(expression, variable, start, end)`

---

## 9. Built-in Functions Catalog

### Complete list of all `preserve="true"` functions observed:

| Function | args | Category | Files |
|----------|------|----------|-------|
| `abs` | 1 | Math | ChordMethod, Dichotomy, RungeKutta5 |
| `augment` | 2 | Matrix | RungeKutta5 |
| `cinterp` | 3 | Interpolation | RungeKutta5 |
| `col` | 2 | Matrix | RungeKutta5, GravitationAcceleration |
| `cols` | 1 | Matrix | Beam, RungeKutta5, SylvesterFormula |
| `concat` | 2 | String | Beam, RomanNumerals |
| `cos` | 1 | Trig | PlanetaryGear, LegendrePolynomials |
| `csort` | 2 | Matrix | GravitationAcceleration |
| `description` | 1 | Display | GravitationAcceleration |
| `det` | 1 | Matrix | Hessian |
| `diff` | 2 | Calculus | ChordMethod, LegendrePolynomials, HermitePolynomials |
| `diff` | 3 | Calculus | HermitePolynomials (nth derivative) |
| `el` | 2 | Matrix | Thomas, Simpson, RungeKutta5 |
| `el` | 3 | Matrix | Beam, Hessian, Jacobian, SylvesterFormula, GravitationAcceleration |
| `eval` | 1 | Evaluation | PlanetaryGear, RungeKutta5, SylvesterFormula |
| `for` | 3 | Control | Thomas (with range) |
| `for` | 4 | Control | Beam, RungeKutta5, SylvesterFormula, Hessian, Jacobian |
| `identity` | 1 | Matrix | SylvesterFormula |
| `if` | 3 | Control | ChordMethod, Dichotomy, RungeKutta5, RomanNumerals |
| `int` | 4 | Calculus | Simpson (definite integration) |
| `line` | N+2 | Control | ChordMethod, Dichotomy, RungeKutta5, Beam, Thomas, RomanNumerals |
| `mat` | N+2 | Matrix | All files with matrices |
| `max` | 1 | Math | RungeKutta5 |
| `min` | 1 | Math | RungeKutta5 |
| `mod` | 2 | Math | Dichotomy, EuclideanGCD, RomanNumerals |
| `num2str` | 1 | String | Beam |
| `polyroots` | 1 | Math | LaguerrePolynomials, SylvesterFormula |
| `product` | 4 | Iteration | SylvesterFormula |
| `range` | 2–3 | Control | Thomas, GravitationAcceleration, MaclaurinSeries |
| `row` | 2 | Matrix | RungeKutta5 |
| `rows` | 1 | Matrix | Thomas, GravitationAcceleration |
| `sign` | 1 | Math | Beam |
| `sin` | 1 | Trig | RungeKutta5, PlanetaryGear |
| `stack` | 2+ | Matrix | Beam, RungeKutta5, PlanetaryGear, SylvesterFormula |
| `sum` | 4 | Iteration | Beam, Simpson, SylvesterFormula, MaclaurinSeries |
| `sys` | varies | Plot | Beam, PlanetaryGear, HermitePolynomials, LegendrePolynomials |
| `tr` | 1 | Matrix | SylvesterFormula |
| `transpose` | 1 | Matrix | RungeKutta5 |
| `while` | 2 | Control | ChordMethod, Dichotomy, EuclideanGCD, RomanNumerals |

### User-defined functions observed:

| Function | args | File | Purpose |
|----------|------|------|---------|
| `f` | 1–2 | ChordMethod, RungeKutta5 | User equation |
| `y` | 1 | RungeKutta5 | ODE solution |
| `base.L` | 1 | Beam | Support drawing |
| `arrow.F` | 2 | Beam | Force arrow drawing |
| `arrow.Q` | 2 | Beam | Distributed load arrow |
| `rect.Q` | 3 | Beam | Load rectangle |
| `ground.op` | 2 | Beam | Ground hatch drawing |
| `gravity` | 6 | GravitationAcceleration | Gravity calculation |
| `H` | 2 | HermitePolynomials | Hermite polynomial |
| `L` | 2 | LaguerrePolynomials | Laguerre polynomial |
| `P` | 2 | LegendrePolynomials | Legendre polynomial |

---

## 10. Version Differences

### v0.96 Files
**Files:** Thomas.sm, RungeKutta5.sm, EuclideanGCD.sm, ChordMethod.sm, Dichotomy.sm, HermitePolynomials.sm, Jacobian.sm, LaguerrePolynomials.sm, LegendrePolynomials.sm, MaclaurinSeries.sm, RomanNumerals.sm, Simpson.sm

- `progid="SMath Studio"` (not "Desktop")
- Root element: `<regions>`
- `<settings>` — no `dpi` attribute
- `<dependences>` (typo preserved)
- All functions have `preserve="true"` on built-ins

### v0.98 Files
**Files:** Beam.sm, GravitationAcceleration.sm, Hessian.sm, PlanetaryGear.sm, SylvesterFormula.sm

- `progid="SMath Studio Desktop"`
- Root element: `<regions>`
- `<settings dpi="96">`
- `<dependencies>` (correctly spelled)
- Some built-in functions lack `preserve="true"` (e.g., `mat`, `el`, `cols` in Beam.sm use `<e type="function" args="N">` without preserve)

### v0.99 Files
**Files:** Newton.sm

- `progid="SMath Studio Desktop"`
- Root element: **`<worksheet>`** (not `<regions>`)
- `<settings ppi="96">` (not `dpi`)
- `<dependencies>` (correctly spelled)
- Regions wrapped in `<regions type="content">`
- Some built-in functions lack `preserve="true"`

### Compatibility Matrix

| Feature | v0.96 | v0.98 | v0.99 |
|---------|-------|-------|-------|
| Root element | `<regions>` | `<regions>` | `<worksheet>` |
| Settings DPI | none | `dpi="96"` | `ppi="96"` |
| Dependencies tag | `<dependences>` | `<dependencies>` | `<dependencies>` |
| `preserve` on builtins | Always | Sometimes missing | Sometimes missing |
| Regions wrapper | none | none | `<regions type="content">` |

---

## 11. Appendix: Per-File Inventory

### Beam.sm (v0.98, 1398 lines)
- **Features:** Units (m, cm, kN, kN/m, dm), matrices with units, collapsible `<area>` regions (2), plot region (2D lines, no grid/axes), `<contract>` for unit conversion, `sum` with index, nested `for` loops, `stack`, `mat`, `el`, `cols`, `sign`, `num2str`, `concat`, `sys`, user-defined drawing functions, string operands for colors, `showInputData="False"`, multilingual (rus/eng/ind)
- **Unique:** `<contract>` element, `num2str`, complex diagram construction with parametric shapes

### ChordMethod.sm (v0.96)
- **Features:** `while` loop, `if` conditional, `line` block, `diff`, `abs`, `≡` equation definition, scientific notation in results
- **Unique:** Root-finding algorithm pattern

### Dichotomy.sm (v0.96)
- **Features:** `while`/`if`/`line`, `mod`, `&` (AND), `≤`, `≠` comparison operators
- **Unique:** Bisection method, multiple comparison operators

### EuclideanGCD.sm (v0.96)
- **Features:** `while`, `&` AND, `mod`, smallest file
- **Unique:** Simplest control flow example

### GravitationAcceleration.sm (v0.98)
- **Features:** Picture region (base64 PNG), `<description>` in math, string operands, complex units (m³/(kg·s²)), `col`/`rows`/`el`/`csort`/`range`/`for`, result formatting (`decimalPlaces`, `significantDigitsMode`, `trailingZeros`)
- **Unique:** Only file with picture region, `<description>` element, extensive result formatting attributes

### HermitePolynomials.sm (v0.96)
- **Features:** `diff` with 3 args (nth derivative), `for` with range, plot with `sys` function, symbolic results
- **Unique:** Higher-order differentiation, `sys` for plot data generation

### Hessian.sm (v0.98)
- **Features:** Nested `for` loops, `el` with 3 args, `diff` for partial derivatives, `det`, symbolic + numeric results
- **Unique:** Matrix of partial derivatives

### Jacobian.sm (v0.96)
- **Features:** Nested `for` loops, matrix construction via loops, `el` with 3 args, `diff`
- **Unique:** Similar pattern to Hessian, matrix filling loop

### LaguerrePolynomials.sm (v0.96)
- **Features:** `polyroots`, `for` with range, `diff`, plot region
- **Unique:** Polynomial root finding

### LegendrePolynomials.sm (v0.96)
- **Features:** Rodrigues' formula, `diff`, `!` factorial, `cos`, plot
- **Unique:** Factorial operator usage

### MaclaurinSeries.sm (v0.96)
- **Features:** `sum` with index, `range`, `for`, `!` factorial, plot
- **Unique:** Series expansion, clean sum/range example

### Newton.sm (v0.99)
- **Features:** v0.99 format (`<worksheet>` root, `ppi`, `<regions type="content">`), `while`, `if`, `diff`, `abs`, `line`
- **Unique:** Only v0.99 file, format reference for modern schema, Greek metadata

### PlanetaryGear.sm (v0.98)
- **Features:** `<area>` collapsible regions, `<area collapsed="true"/>`, plot with `animate="t"`, `eval`, `stack`, `≡` operator, string operands for plot styling, `sys`, `cos`, `sin`
- **Unique:** Animation, multi-area document, plot styling with string operands

### RomanNumerals.sm (v0.96)
- **Features:** `concat` string, `description` function (appears to annotate), `style="string"` operands, nested `while`/`for`/`if`
- **Unique:** String manipulation, complex nesting

### RungeKutta5.sm (v0.96, 790 lines)
- **Features:** Complex `for` loop with `while`-style condition, adaptive step algorithm, `if`/`line` nesting (10 args!), `augment`, `stack`, `cols`, `col`, `row`, `transpose`, `cinterp`, `min`, `max`, `abs`, `eval`, `sin`, plot regions
- **Unique:** Deepest control flow nesting, largest `line` args count (10), adaptive step-size logic

### Simpson.sm (v0.96)
- **Features:** `sum` with index, `int` built-in integration, `range`, simple structure
- **Unique:** Comparison of numerical (`sum`) vs built-in (`int`) integration

### SylvesterFormula.sm (v0.98)
- **Features:** `tr` (trace), `identity`, `polyroots`, `eval`, `product`, `cols`, `sum`, nested `for`, matrices
- **Unique:** Matrix exponential via Sylvester formula, `product` function

### Thomas.sm (v0.96, 680 lines)
- **Features:** `for` with `range`, `line`, `el` (2 args), `rows`, `≡` equation definition, symbolic results (fractions)
- **Unique:** Tridiagonal matrix algorithm, backward substitution with descending `range`

---

## Key Implementation Insights for `smathpy`

### Priority Findings

1. **RPN args counting for `mat`**: `args = rows × cols + 2`. But each "element" can be a multi-token sub-expression. The builder must track stack depth, not `<e>` count.

2. **`line` function args**: `args = num_statements + 2`. The last two stack items before `line` are the statement count and `1`.

3. **`for` loop has two forms**: `args=4` (init, condition, increment, body) and `args=3` (variable, range, body).

4. **Bracket elements are display hints only**: They don't change evaluation. Place them after the sub-expression they wrap, before the consuming operator.

5. **`preserve="true"` is inconsistent across versions**: The builder should always emit it for known built-in functions for maximum compatibility.

6. **`<contract>` block**: A third component in `<math>` (alongside `<input>` and `<result>`) that specifies output unit conversion. Must be included in the `MathRegion` model.

7. **Area regions nest**: Child regions go inside the parent `<region>` element, between `<area collapsed="true"/>` and the terminator region containing `<area terminator="true"/>`.

8. **`stack` has variable args**: Usually 2, but can be 3+ (Beam.sm uses `stack` with 3 args).

9. **User vs built-in function names can use dots**: `base.L`, `arrow.F`, `rect.Q`, `ground.op` are all valid function names.

10. **Version detection strategy**: Check if root is `<worksheet>` (v0.99+) or `<regions>` (v0.96-0.98). Check for `<dependences>` vs `<dependencies>`. The builder should target v0.98 format (modern but compatible).

### Recommended Default Settings

Based on the most common patterns across all 18 files:

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<?application progid="SMath Studio Desktop" version="0.98.6606.22069"?>
<regions xmlns="http://smath.info/schemas/worksheet/1.0">
  <settings dpi="96">
    <identity>
      <id>{generated-uuid}</id>
      <revision>1</revision>
    </identity>
    <metadata lang="eng">
      <title>{title}</title>
      <author>{author}</author>
    </metadata>
    <calculation>
      <precision>4</precision>
      <exponentialThreshold>5</exponentialThreshold>
      <fractions>decimal</fractions>
    </calculation>
    <pageModel active="false" printAreas="true" simpleEqualsOnly="false"
               printBackgroundImages="true">
      <paper id="9" orientation="Portrait" width="827" height="1169" />
      <margins left="39" right="39" top="39" bottom="39" />
      <header alignment="Center" color="#a9a9a9">&amp;[DATE] &amp;[TIME] - &amp;[FILENAME]</header>
      <footer alignment="Center" color="#a9a9a9">&amp;[PAGENUM] / &amp;[COUNT]</footer>
      <backgrounds />
    </pageModel>
    <dependencies>
      <assembly name="SMath Studio Desktop" version="0.98.6606.22069"
                guid="a37cba83-b69c-4c71-9992-55ff666763bd" />
      <assembly name="Math Region" version="0.98.6606.22069"
                guid="02f1ab51-215b-466e-a74d-5d8b1cf85e8d" />
      <assembly name="Text Region" version="1.10.6606.22071"
                guid="485d28c5-349a-48b6-93be-12a35a1c1e39" />
      <assembly name="Special Functions" version="1.11.6606.22071"
                guid="2814e667-4e12-48b1-8d51-194e480eabc5" />
    </dependencies>
  </settings>
  <!-- regions here -->
</regions>
```
