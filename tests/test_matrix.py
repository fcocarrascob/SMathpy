"""Tests for matrix construction and operations."""

from smathpy.expression import (
    var, num,
    mat, el, rows, cols, row, col, transpose, det, tr, identity,
    augment, stack,
)


class TestMatrixConstruction:
    def test_simple_2x2(self):
        """mat([[1,2],[3,4]]) → 1 2 3 4 2 2 mat{6}"""
        expr = mat([[1, 2], [3, 4]])
        vals = [e.value for e in expr.elements]
        assert vals == ["1", "2", "3", "4", "2", "2", "mat"]
        assert expr.elements[-1].args == 6  # 2*2 + 2

    def test_3x2(self):
        """3x2 matrix → 6 data + 2 = args 8"""
        expr = mat([[1, 2], [3, 4], [5, 6]])
        assert expr.elements[-1].args == 8  # 3*2 + 2

    def test_matrix_with_expressions(self):
        """Matrix cells can be full expressions."""
        x = var("x")
        expr = mat([[x + 1, x * 2], [0, 1]])
        # x 1 + x 2 * 0 1 2 2 mat{6}
        assert expr.elements[-1].args == 6

    def test_empty_matrix_raises(self):
        import pytest
        with pytest.raises(ValueError):
            mat([])

    def test_uneven_rows_raises(self):
        import pytest
        with pytest.raises(ValueError):
            mat([[1, 2], [3]])


class TestMatrixAccess:
    def test_el_1d(self):
        """el(v, i) → v i el{2}"""
        expr = el("v", "i")
        assert expr.elements[-1].args == 2

    def test_el_2d(self):
        """el(A, i, j) → A i j el{3}"""
        expr = el("A", "i", "j")
        assert expr.elements[-1].args == 3


class TestMatrixOps:
    def test_rows(self):
        expr = rows("A")
        assert expr.elements[-1].value == "rows"
        assert expr.elements[-1].args == 1

    def test_cols(self):
        expr = cols("A")
        assert expr.elements[-1].value == "cols"

    def test_transpose(self):
        expr = transpose("A")
        assert expr.elements[-1].value == "transpose"

    def test_det(self):
        expr = det("A")
        assert expr.elements[-1].value == "det"

    def test_trace(self):
        expr = tr("A")
        assert expr.elements[-1].value == "tr"

    def test_identity(self):
        expr = identity(3)
        assert expr.elements[-1].value == "identity"

    def test_augment(self):
        expr = augment("A", "B")
        assert expr.elements[-1].value == "augment"
        assert expr.elements[-1].args == 2

    def test_stack(self):
        expr = stack("A", "B")
        assert expr.elements[-1].value == "stack"
        assert expr.elements[-1].args == 2

    def test_stack_three(self):
        expr = stack("A", "B", "C")
        assert expr.elements[-1].args == 3
