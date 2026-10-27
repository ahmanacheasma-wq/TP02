
from academicelement import AcademicElement


class Module(AcademicElement):
    """Represente un module d'enseignement."""

    def __init__(
        self,
        name="",
        title="",
        coef=1,
        credit=1,
        hours_lecture=1.5,
        hours_td=0,
        hours_tp=0,
        teaching_mode="In-person",
        continous_percent=40,
        exam_percent=60
    ):
        super().__init__(name, title)

        self.coef = coef
        self.credit = credit
        self.hours_lecture = hours_lecture
        self.hours_td = hours_td
        self.hours_tp = hours_tp
        self.teaching_mode = teaching_mode

        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent

        self.total_hours = self._WEEKS * (
            hours_lecture + hours_td + hours_tp
        )

        self._grades = {
            "tp": None,
            "td": None,
            "exam": None
        }

    def set_grade(self, tp=None, td=None, exam=None):
        """Modifie les notes de maniere controlee."""
        for name, grade in (
            ("tp", tp),
            ("td", td),
            ("exam", exam)
        ):
            if grade is not None:
                if not 0 <= grade <= 20:
                    raise ValueError("La note doit etre entre 0 et 20.")
                self._grades[name] = grade

    def summary(self):
        """Retourne un resume du module."""
        return (
            f"Module: {self.name} - {self.title}\n"
            f"Coefficient: {self.coef}\n"
            f"Credits: {self.credit}\n"
            f"Heures totales: {self.total_hours}\n"
            f"Cours: {self.hours_lecture}, "
            f"TD: {self.hours_td}, TP: {self.hours_tp}\n"
            f"Mode: {self.teaching_mode}\n"
            f"Evaluation continue: "
            f"{self.evaluation_continous_percent}%\n"
            f"Examen: {self.evaluation_exam_percent}%"
        )

    def calculate_average(self):
        """Calcule la moyenne ponderee du module."""
        tp = self._grades["tp"]
        td = self._grades["td"]
        exam = self._grades["exam"]

        if exam is None:
            return 0

        continuous = self.evaluation_continous_percent
        exam_percent = self.evaluation_exam_percent

        if self.hours_tp and self.hours_td:
            tp_percent = continuous / 2
            td_percent = continuous / 2
        elif self.hours_tp:
            tp_percent = continuous
            td_percent = 0
        elif self.hours_td:
            tp_percent = 0
            td_percent = continuous
        else:
            tp_percent = 0
            td_percent = 0

        average = (
            (tp or 0) * tp_percent / 100
            + (td or 0) * td_percent / 100
            + exam * exam_percent / 100
        )

        return average

    def calculate_credits(self):
        """Attribue les credits si la moyenne atteint 10/20."""
        if self.calculate_average() >= 10:
            return self.credit
        return 0


if __name__ == "__main__":
    mti = Module(
        name="MTI",
        title="Methods and Technologies of Implementation",
        coef=3,
        credit=5,
        hours_lecture=1.5,
        hours_tp=1.5,
        teaching_mode="In-person"
    )

    mti.set_grade(tp=10, exam=12)

    print(mti.summary())
    print("Module average:", mti.name, mti.calculate_average())
    print("Module credits:", mti.calculate_credits())
