"""Tests for control structures: for, while, if, line, range, sum, product."""

from smathpy.expression import (
    var, num, assign,
    line, range_, for_range, for_loop, while_loop, if_, sum_, product_,
)


class TestLine:
    def test_line_block(self):
        """line(s1, s2) → s1 s2 2 1 line{4}"""
        s1 = assign("x", 1)
        s2 = assign("y", 2)
        expr = line(s1, s2)
        vals = [e.value for e in expr.elements]
        # x 1 : y 2 : 2 1 line
        assert vals[-1] == "line"
        assert vals[-3] == "2"  # statement count
        assert vals[-2] == "1"  # always 1
        assert expr.elements[-1].args == 4  # N+2 = 2+2

    def test_line_three_statements(self):
        expr = line(assign("a", 1), assign("b", 2), assign("c", 3))
        assert expr.elements[-1].args == 5  # 3+2


class TestRange:
    def test_range_two_args(self):
        """range(1, n) → 1 n range{2}"""
        expr = range_(1, "n")
        vals = [e.value for e in expr.elements]
        assert vals == ["1", "n", "range"]
        assert expr.elements[-1].args == 2

    def test_range_three_args(self):
        """range(1, n, 2) → 1 n 2 range{3}"""
        expr = range_(1, "n", 2)
        assert expr.elements[-1].args == 3


class TestForLoop:
    def test_for_with_range(self):
        """for(i, range(1,n), body) → i range_elems body for{3}"""
        body = assign("s", var("s") + var("i"))
        expr = for_range("i", range_(1, "n"), body)
        assert expr.elements[-1].value == "for"
        assert expr.elements[-1].args == 3

    def test_for_explicit(self):
        """for with init/condition/increment (4-arg form)."""
        i = var("i")
        expr = for_loop(
            "i",
            start=num(1),
            condition=i <= var("n"),
            increment=i + 1,
            body=assign("s", var("s") + i),
        )
        assert expr.elements[-1].value == "for"
        assert expr.elements[-1].args == 4


class TestWhileLoop:
    def test_while(self):
        """while(condition, body) → cond body while{2}"""
        cond = var("x") > 0
        body = assign("x", var("x") - 1)
        expr = while_loop(cond, body)
        assert expr.elements[-1].value == "while"
        assert expr.elements[-1].args == 2


class TestIf:
    def test_if_conditional(self):
        """if(cond, true, false) → cond true false if{3}"""
        cond = var("x") > 0
        expr = if_(cond, var("a"), var("b"))
        assert expr.elements[-1].value == "if"
        assert expr.elements[-1].args == 3


class TestSumProduct:
    def test_sum(self):
        """sum(expr, k, 1, n) → expr k 1 n sum{4}"""
        expr = sum_(var("k") ** 2, "k", 1, "n")
        assert expr.elements[-1].value == "sum"
        assert expr.elements[-1].args == 4

    def test_product(self):
        """product(expr, k, 0, n) → expr k 0 n product{4}"""
        expr = product_(var("k"), "k", 0, "n")
        assert expr.elements[-1].value == "product"
        assert expr.elements[-1].args == 4
