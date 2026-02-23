"""Matrix construction and operations."""

from __future__ import annotations

from .builder import Expr, ExprLike, coerce, call
from .elements import Element, function, operand


def mat(rows_data: list[list[ExprLike]]) -> Expr:
    """Build a matrix expression from a 2D list.

    ``mat([[1, 2], [3, 4]])`` → 1×2 matrix RPN with mat(6) = 4 data + 2 dims.

    Args:
        rows_data: 2D list where rows_data[i][j] is the element at row i, col j.
    """
    n_rows = len(rows_data)
    if n_rows == 0:
        raise ValueError("Matrix must have at least one row")
    n_cols = len(rows_data[0])
    if n_cols == 0:
        raise ValueError("Matrix must have at least one column")
    if any(len(row) != n_cols for row in rows_data):
        raise ValueError("All rows must have the same number of columns")

    elems: list = []
    for row in rows_data:
        for cell in row:
            elems.extend(coerce(cell)._elements)

    # Push rows and cols counts, then mat function
    # args = (num_data_elements pushed as individual stack values) + 2
    # but each cell is ONE stack value regardless of how many elements it has
    total_args = n_rows * n_cols + 2
    elems.append(operand(n_rows))
    elems.append(operand(n_cols))
    elems.append(function("mat", total_args))
    return Expr(elems)


def el(matrix: Expr | str, *indices: ExprLike) -> Expr:
    """Element access: el(M, i) or el(M, i, j)."""
    return call("el", matrix, *indices)


def rows(matrix: Expr | str) -> Expr:
    """Number of rows in a matrix."""
    return call("rows", matrix)


def cols(matrix: Expr | str) -> Expr:
    """Number of columns in a matrix."""
    return call("cols", matrix)


def row(matrix: Expr | str, index: ExprLike) -> Expr:
    """Extract row i from a matrix."""
    return call("row", matrix, index)


def col(matrix: Expr | str, index: ExprLike) -> Expr:
    """Extract column j from a matrix."""
    return call("col", matrix, index)


def transpose(matrix: Expr | str) -> Expr:
    """Matrix transpose."""
    return call("transpose", matrix)


def det(matrix: Expr | str) -> Expr:
    """Matrix determinant."""
    return call("det", matrix)


def tr(matrix: Expr | str) -> Expr:
    """Matrix trace."""
    return call("tr", matrix)


def identity(n: ExprLike) -> Expr:
    """Identity matrix of size n."""
    return call("identity", n)


def augment(a: Expr | str, b: Expr | str) -> Expr:
    """Horizontally append matrices."""
    return call("augment", a, b)


def stack(*matrices: Expr | str) -> Expr:
    """Vertically stack matrices."""
    return call("stack", *matrices)


def csort(matrix: Expr | str, col_idx: ExprLike) -> Expr:
    """Sort matrix by column col_idx."""
    return call("csort", matrix, col_idx)


def polyroots(coefficients: Expr | str) -> Expr:
    """Polynomial roots from coefficient vector."""
    return call("polyroots", coefficients)


def cinterp(data: Expr | str, col_x: ExprLike,
            col_y: ExprLike) -> Expr:
    """Cubic spline interpolation."""
    return call("cinterp", data, col_x, col_y)
