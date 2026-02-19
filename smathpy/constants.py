"""SMath XML format constants."""

# XML Namespace
SMATH_NAMESPACE = "http://smath.info/schemas/worksheet/1.0"
NS = {"sm": SMATH_NAMESPACE}

# Application info (targeting v0.98 — modern and widely compatible)
APP_PROGID = "SMath Studio Desktop"
APP_VERSION = "0.98.6606.22069"

# Known assembly definitions
ASSEMBLIES = {
    "SMath Studio Desktop": {
        "version": "0.98.6606.22069",
        "guid": "a37cba83-b69c-4c71-9992-55ff666763bd",
    },
    "Math Region": {
        "version": "0.98.6606.22069",
        "guid": "02f1ab51-215b-466e-a74d-5d8b1cf85e8d",
    },
    "Text Region": {
        "version": "1.10.6606.22071",
        "guid": "485d28c5-349a-48b6-93be-12a35a1c1e39",
    },
    "Special Functions": {
        "version": "1.11.6606.22071",
        "guid": "2814e667-4e12-48b1-8d51-194e480eabc5",
    },
    "Plot Region": {
        "version": "1.9.6606.22072",
        "guid": "c451c2b5-798b-4f08-b9ec-b90963d1ddaa",
    },
}

# Default assemblies included in every document
DEFAULT_ASSEMBLIES = [
    "SMath Studio Desktop",
    "Math Region",
    "Text Region",
    "Special Functions",
]

# Default colors
COLOR_BLACK = "#000000"
COLOR_BLUE = "#0000ff"
COLOR_WHITE = "#ffffff"
COLOR_GRAY_BG = "#dddddd"
COLOR_YELLOW = "#ffff80"
COLOR_GREEN = "#80ff80"
COLOR_HEADER = "#a9a9a9"
COLOR_BROWN = "#804040"

# Default font sizes
FONT_TITLE = 12
FONT_DEFAULT = 10

# Default layout constants
DEFAULT_LEFT = 9
DEFAULT_TOP_START = 9
LINE_HEIGHT = 27  # spacing between regions vertically

# Built-in functions that require preserve="true"
BUILTIN_FUNCTIONS = {
    "abs", "augment", "cinterp", "col", "cols", "concat", "cos", "csort",
    "description", "det", "diff", "el", "eval", "for", "identity", "if",
    "int", "line", "mat", "max", "min", "mod", "num2str", "polyroots",
    "product", "range", "row", "rows", "sign", "sin", "sqrt", "stack",
    "sum", "sys", "tan", "tr", "transpose", "while", "exp", "ln", "log",
    "asin", "acos", "atan", "ceil", "floor", "round", "re", "im",
    "length", "submatrix", "reverse", "sort", "numer", "denom",
    "linterp", "solve", "numstr",
}

# Paper sizes
PAPER_LETTER = {"id": "1", "width": "850", "height": "1100"}
PAPER_A4 = {"id": "9", "width": "827", "height": "1169"}
