
import pytest
from module import Module
from unit import Unit


def test_unit_average():
    m1 = Module("M1", "Module 1", coef=3, credit=5, hours_tp=1.5)
    m1.set_grade(tp=10, exam=12)

    m2 = Module("M2", "Module 2", coef=2, credit=4, hours_tp=1.5)
    m2.set_grade(tp=8, exam=6)

    unit = Unit("UE1", "Unite 1", [m1, m2])

    assert unit.calculate_average() == pytest.approx(9.44)


def test_unit_credits():
    m = Module("M1", "Module 1", credit=5, hours_tp=1.5)
    m.set_grade(tp=10, exam=12)

    unit = Unit("UE1", "Unite 1", [m])
    assert unit.calculate_credits() == 5
