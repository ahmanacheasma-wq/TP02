
import pytest
from module import Module


def test_module_average():
    m = Module(
        "MTI", "Methods and Technologies of Implementation",
        coef=3, credit=5, hours_tp=1.5
    )
    m.set_grade(tp=10, exam=12)
    assert m.calculate_average() == pytest.approx(11.2)


def test_module_credits():
    m = Module(
        "MTI", "Methods and Technologies of Implementation",
        credit=5, hours_tp=1.5
    )
    m.set_grade(tp=10, exam=12)
    assert m.calculate_credits() == 5


def test_invalid_grade():
    m = Module("MTI", "Methods")
    with pytest.raises(ValueError):
        m.set_grade(exam=25)
