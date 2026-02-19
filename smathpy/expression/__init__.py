"""Expression package — building RPN expressions for SMath worksheets."""

from .builder import (
    Expr,
    assign,
    call,
    const,
    define,
    evaluate,
    func_assign,
    num,
    placeholder,
    string,
    unit,
    var,
)
from .control import (
    for_loop,
    for_range,
    if_,
    line,
    product_,
    range_,
    sum_,
    while_loop,
)
from .elements import (
    Element,
    bracket,
    function,
    operand,
    operator,
    string_operand,
    unit_operand,
)
from .functions import (
    abs_,
    acos,
    asin,
    atan,
    ceil,
    concat,
    cos,
    diff,
    diff_n,
    eval_,
    exp,
    floor,
    integral,
    ln,
    log,
    max_,
    min_,
    mod,
    num2str,
    round_,
    sign,
    sin,
    sqrt,
    tan,
)
from .matrix import (
    augment,
    cinterp,
    col,
    cols,
    csort,
    det,
    el,
    identity,
    mat,
    polyroots,
    row,
    rows,
    stack,
    tr,
    transpose,
)

__all__ = [
    # builder
    "Expr", "var", "num", "const", "string", "unit", "placeholder",
    "assign", "define", "func_assign", "evaluate", "call",
    # elements
    "Element", "operand", "operator", "function", "bracket",
    "unit_operand", "string_operand",
    # functions
    "abs_", "sign", "sqrt", "exp", "ln", "log", "ceil", "floor", "round_",
    "mod", "max_", "min_",
    "sin", "cos", "tan", "asin", "acos", "atan",
    "diff", "diff_n", "integral",
    "concat", "num2str", "eval_",
    # matrix
    "mat", "el", "rows", "cols", "row", "col", "transpose", "det", "tr",
    "identity", "augment", "stack", "csort", "polyroots", "cinterp",
    # control
    "line", "range_", "for_range", "for_loop", "while_loop", "if_",
    "sum_", "product_",
]
