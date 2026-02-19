"""Matrix construction and operations."""

from __future__ import annotations

from typing import List, Union

from .builder import Expr, _coerce, call
from .elements import Element, function, operand


def mat(rows_data: List[List[Union[Expr, int, float, str]]]) -> Expr:
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
            elems.extend(_coerce(cell)._elements)

    # Push rows and cols counts, then mat function
    # args = (num_data_elements pushed as individual stack values) + 2
    # but each cell is ONE stack value regardless of how many elements it has
    total_args = n_rows * n_cols + 2
    elems.append(operand(n_rows))
    elems.append(operand(n_cols))
    elems.append(function("mat", total_args))
    return Expr(elems)


def el(matrix: Union[Expr, str], *indices: Union[Expr, int, float, str]) -> Expr:
    """Element access: el(M, i) or el(M, i, j)."""
    return call("el", matrix, *indices)


def rows(matrix: Union[Expr, str]) -> Expr:
    return call("rows", matrix)


def cols(matrix: Union[Expr, str]) -> Expr:
    return call("cols", matrix)


def row(matrix: Union[Expr, str], index: Union[Expr, int, float, str]) -> Expr:
    return call("row", matrix, index)


def col(matrix: Union[Expr, str], index: Union[Expr, int, float, str]) -> Expr:
    return call("col", matrix, index)


def transpose(matrix: Union[Expr, str]) -> Expr:
    return call("transpose", matrix)


def det(matrix: Union[Expr, str]) -> Expr:
    return call("det", matrix)


def tr(matrix: Union[Expr, str]) -> Expr:
    """Matrix trace."""
    return call("tr", matrix)


def identity(n: Union[Expr, int, float, str]) -> Expr:
    return call("identity", n)


def augment(a: Union[Expr, str], b: Union[Expr, str]) -> Expr:
    """Horizontally append matrices."""
    return call("augment", a, b)


def stack(*matrices: Union[Expr, str]) -> Expr:
    """Vertically stack matrices."""
    return call("stack", *matrices)


def csort(matrix: Union[Expr, str], col_idx: Union[Expr, int, float, str]) -> Expr:
    return call("csort", matrix, col_idx)


def polyroots(coefficients: Union[Expr, str]) -> Expr:
    return call("polyroots", coefficients)


def cinterp(data: Union[Expr, str], col_x: Union[Expr, int, float, str],
            col_y: Union[Expr, int, float, str]) -> Expr:
    return call("cinterp", data, col_x, col_y)
