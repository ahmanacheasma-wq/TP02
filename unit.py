
from academicelement import AcademicElement


class Unit(AcademicElement):
    """Represente une unite d'enseignement."""

    def __init__(self, name, title, modules=None):
        super().__init__(name, title)
        self._modules = list(modules) if modules else []

    def add_module(self, module):
        """Ajoute un module a l'unite."""
        if not isinstance(module, AcademicElement):
            raise TypeError("L'element doit etre academique.")
        self._modules.append(module)

    def calculate_average(self):
        """Calcule la moyenne ponderee par les coefficients."""
        if not self._modules:
            return 0

        total_coef = sum(m.coef for m in self._modules)

        if total_coef == 0:
            return 0

        total = sum(
            m.calculate_average() * m.coef
            for m in self._modules
        )

        return total / total_coef

    def calculate_credits(self):
        """Calcule les credits obtenus dans l'unite."""
        if self.calculate_average() >= 10:
            return sum(m.credit for m in self._modules)

        return sum(m.calculate_credits() for m in self._modules)


if __name__ == "__main__":
    from module import Module

    m1 = Module(
        "MTI", "Methods and Technologies of Implementation",
        coef=3, credit=5, hours_tp=1.5
    )
    m1.set_grade(tp=10, exam=12)

    m2 = Module(
        "AABD", "Architecture et administration des bases de donnees",
        coef=2, credit=4, hours_tp=1.5
    )
    m2.set_grade(tp=8, exam=6)

    u1 = Unit("UEM11", "UE Methodologie", [m1, m2])

    print("Unit:", u1.name, u1.title)
    print("Unit average:", u1.calculate_average())
    print("Unit credits:", u1.calculate_credits())
