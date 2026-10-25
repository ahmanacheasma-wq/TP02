
class Module:
    """
    Represents a teaching module with pedagogical
    and evaluation attributes.
    """

    def __init__(
        self,
        name: str = "",
        title: str = "",
        coef: int = 1,
        credit: int = 1,
        hours_lecture: float = 1.5,
        hours_td: float = 0,
        hours_tp: float = 0,
        teaching_mode: str = "In-person",
        continous_percent: int = 40,
        exam_percent: int = 60
    ):
        self._WEEKS = 15

        # Basic attributes
        self.name = name
        self.title = title
        self.coef = coef
        self.credit = credit

        # Workload distribution
        self.hours_lecture = hours_lecture
        self.hours_td = hours_td
        self.hours_tp = hours_tp

        # Teaching and evaluation mode
        self.teaching_mode = teaching_mode
        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent

        # Total hours per semester
        self.total_hours = self._WEEKS * (
            self.hours_lecture
            + self.hours_td
            + self.hours_tp
        )

        # Grades
        self._grades = {
            "tp": None,
            "td": None,
            "exam": None
        }

    def set_grade(self, tp=None, td=None, exam=None):
        """Set the grades of the module."""

        if tp is not None:
            self._grades["tp"] = tp

        if td is not None:
            self._grades["td"] = td

        if exam is not None:
            self._grades["exam"] = exam

    def summary(self):
        """Return a summary of the module."""

        return (
            f"Module: {self.title} ({self.name})\n"
            f"Coefficient: {self.coef}, Credits: {self.credit}\n"
            f"Hours: total {self.total_hours}, "
            f"{self.hours_lecture} Lecture, "
            f"{self.hours_td} TD, "
            f"{self.hours_tp} TP\n"
            f"Teaching mode: {self.teaching_mode}, "
            f"Evaluation mode: Continuous: "
            f"{self.evaluation_continous_percent}% "
            f"Exam: {self.evaluation_exam_percent}%"
        )

    def calculate_average(self):
        """Calculate the weighted average of the module."""

        tp = self._grades["tp"] or 0
        td = self._grades["td"] or 0
        exam = self._grades["exam"] or 0

        percent_exam = self.evaluation_exam_percent
        percent_tp = 0
        percent_td = 0

        if self.hours_tp and self.hours_td:
            percent_tp = self.evaluation_continous_percent / 2
            percent_td = self.evaluation_continous_percent / 2

        elif self.hours_tp:
            percent_tp = self.evaluation_continous_percent

        elif self.hours_td:
            percent_td = self.evaluation_continous_percent

        return (
            tp * percent_tp / 100
            + td * percent_td / 100
            + exam * percent_exam / 100
        )

    def calculate_credits(self):
        """Calculate the credits obtained for this module."""

        average = self.calculate_average()

        if average >= 10:
            return self.credit

        return 0


# Example usage
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

    print(mti.summary())

    # Set grades
    mti.set_grade(tp=10, exam=12)

    # Display average and credits
    print("Average:", mti.calculate_average())
    print("Credits obtained:", mti.calculate_credits())
