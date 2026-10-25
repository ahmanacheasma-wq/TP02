
from abc import ABC, abstractmethod


class AcademicElement(ABC):
    def __init__(self, name, title):
        self.name = name
        self.title = title

    @abstractmethod
    def calculate_average(self):
        pass

    @abstractmethod
    def calculate_credits(self):
        pass


class Module(AcademicElement):
    def __init__(self, name="", title="", coef=1, credit=1,
                 hours_lecture=1.5, hours_td=0, hours_tp=0,
                 teaching_mode="In-person",
                 continous_percent=40, exam_percent=60):
        super().__init__(name, title)
        self._WEEKS = 15
        self.coef = coef
        self.credit = credit
        self.hours_lecture = hours_lecture
        self.hours_td = hours_td
        self.hours_tp = hours_tp
        self.teaching_mode = teaching_mode
        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent
        self.total_hours = self._WEEKS * (
            self.hours_lecture + self.hours_td + self.hours_tp
        )
        self._grades = {"tp": None, "td": None, "exam": None}

    def set_grade(self, tp=None, td=None, exam=None):
        if tp is not None:
            self._grades["tp"] = tp
        if td is not None:
            self._grades["td"] = td
        if exam is not None:
            self._grades["exam"] = exam

    def summary(self):
        return (
            f"{self.name} - {self.title} | "
            f"Coefficient: {self.coef} | Credits: {self.credit} | "
            f"Total hours: {self.total_hours}"
        )

    def calculate_average(self):
        tp = self._grades["tp"] or 0
        td = self._grades["td"] or 0
        exam = self._grades["exam"] or 0

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
            + exam * self.evaluation_exam_percent / 100
        )

    def calculate_credits(self):
        if self.calculate_average() >= 10:
            return self.credit
        return 0


class Unit(AcademicElement):
    def __init__(self, name, title, modules=None):
        super().__init__(name, title)
        self._modules = modules if modules is not None else []

    def add_module(self, module):
        self._modules.append(module)

    def calculate_average(self):
        if not self._modules:
            return 0

        total_coef = sum(module.coef for module in self._modules)

        if total_coef == 0:
            return 0

        weighted_sum = sum(
            module.calculate_average() * module.coef
            for module in self._modules
        )

        return weighted_sum / total_coef

    def calculate_credits(self):
        if self.calculate_average() >= 10:
            return sum(module.credit for module in self._modules)

        return sum(
            module.calculate_credits()
            for module in self._modules
        )


class Semester(AcademicElement):
    def __init__(self, name, title, units=None):
        super().__init__(name, title)
        self._units = units if units is not None else []

    def add_unit(self, unit):
        self._units.append(unit)

    def calculate_average(self):
        modules = [
            module
            for unit in self._units
            for module in unit._modules
        ]

        if not modules:
            return 0

        total_coef = sum(module.coef for module in modules)

        if total_coef == 0:
            return 0

        weighted_sum = sum(
            module.calculate_average() * module.coef
            for module in modules
        )

        return weighted_sum / total_coef

    def calculate_credits(self):
        return sum(unit.calculate_credits() for unit in self._units)


def create_module(name, title, coef, credit, hours_td=0,
                  hours_tp=0, teaching_mode="In-person",
                  continous_percent=40, exam_percent=60):
    return Module(
        name=name,
        title=title,
        coef=coef,
        credit=credit,
        hours_lecture=1.5,
        hours_td=hours_td,
        hours_tp=hours_tp,
        teaching_mode=teaching_mode,
        continous_percent=continous_percent,
        exam_percent=exam_percent
    )


def assign_example_grades(module):
    if module.teaching_mode == "Distance":
        module.set_grade(exam=12)
    elif module.hours_tp and module.hours_td:
        module.set_grade(tp=12, td=10, exam=11)
    elif module.hours_tp:
        module.set_grade(tp=12, exam=11)
    elif module.hours_td:
        module.set_grade(td=12, exam=11)
    else:
        module.set_grade(exam=11)


def display_semester(semester):
    print(semester.name, "-", semester.title)
    print("Average:", round(semester.calculate_average(), 2))
    print("Credits obtained:", semester.calculate_credits())

    for unit in semester._units:
        print(
            unit.name,
            "-",
            unit.title,
            "| Average:",
            round(unit.calculate_average(), 2),
            "| Credits:",
            unit.calculate_credits()
        )

        for module in unit._modules:
            print(
                module.name,
                "-",
                module.title,
                "| Average:",
                round(module.calculate_average(), 2),
                "| Credits:",
                module.calculate_credits()
            )

    print()


if __name__ == "__main__":
    uef11 = Unit("UEF11", "UE Fondamentale 11", [
        create_module("F111", "Réseaux des couches basses", 3, 6, 1.5, 1.5),
        create_module("F112", "Algorithmique Avancée et Complexité", 2, 4, 0, 1.5)
    ])

    uef12 = Unit("UEF12", "UE Fondamentale 12", [
        create_module("F121", "Système d'exploitation", 2, 4, 1.5, 0),
        create_module("F122", "Architectures Modernes des Systèmes Informatiques", 2, 4, 0, 1.5)
    ])

    uem11 = Unit("UEM11", "UE Méthodologique 11", [
        create_module("M111", "Architecture et administration des bases de données", 2, 4, 0, 1.5),
        create_module("M112", "Méthodes et Technologies d'Implémentation", 3, 5, 0, 1.5)
    ])

    ued11 = Unit("UED11", "UE Découverte 11", [
        create_module("D111", "Systèmes de Communication Vocaux et Vidéos", 2, 2, 0, 1.5)
    ])

    uet11 = Unit("UET11", "UE Transversale 11", [
        create_module(
            "T111", "Cloud Computing", 1, 1,
            teaching_mode="Distance",
            continous_percent=0,
            exam_percent=100
        )
    ])

    semester1 = Semester(
        "S1",
        "Semestre 1",
        [uef11, uef12, uem11, ued11, uet11]
    )

    uef21 = Unit("UEF21", "UE Fondamentale 21", [
        create_module("F211", "Middlewares pour les systèmes répartis", 3, 6, 1.5, 1.5),
        create_module("F212", "Modélisation et Architectures logicielles", 2, 4, 0, 1.5)
    ])

    uf22 = Unit("UF22", "UE Fondamentale 22", [
        create_module("UF221", "Réseaux de la couche IP", 3, 6, 0, 1.5),
        create_module("UF222", "Introduction au Machine Learning", 2, 4, 0, 1.5)
    ])

    uem21 = Unit("UEM21", "UE Méthodologique 21", [
        create_module("M211", "Infographie", 2, 3, 0, 1.5),
        create_module("M212", "Gestion de l'incertain", 2, 3, 1.5, 0)
    ])

    ued21 = Unit("UED21", "UE Découverte 21", [
        create_module("D211", "Internet of Things", 2, 3, 0, 1.5)
    ])

    uet21 = Unit("UET21", "UE Transversale 21", [
        create_module(
            "T211", "Cybercriminalité", 1, 1,
            teaching_mode="Distance",
            continous_percent=0,
            exam_percent=100
        )
    ])

    semester2 = Semester(
        "S2",
        "Semestre 2",
        [uef21, uf22, uem21, ued21, uet21]
    )

    for semester in [semester1, semester2]:
        for unit in semester._units:
            for module in unit._modules:
                assign_example_grades(module)

    display_semester(semester1)
    display_semester(semester2)

    print("Total credits S1:", sum(
        module.credit
        for unit in semester1._units
        for module in unit._modules
    ))

    print("Total credits S2:", sum(
        module.credit
        for unit in semester2._units
        for module in unit._modules
    ))