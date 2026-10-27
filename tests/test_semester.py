
import pytest
from module import Module
from unit import Unit
from semester import Semester


def test_semester_average():
    m = Module("M1", "Module 1", coef=1, credit=5, hours_tp=1.5)
    m.set_grade(tp=10, exam=12)

    unit = Unit("UE1", "Unite 1", [m])
    semester = Semester("S1", "Semestre 1", [unit])

    assert semester.calculate_average() == pytest.approx(11.2)


def test_semester_credits():
    m = Module("M1", "Module 1", credit=5, hours_tp=1.5)
    m.set_grade(tp=10, exam=12)

    unit = Unit("UE1", "Unite 1", [m])
    semester = Semester("S1", "Semestre 1", [unit])

    assert semester.calculate_credits() == 5
