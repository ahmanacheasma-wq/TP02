
from academicelement import AcademicElement


class Semester(AcademicElement):
    """Represente un semestre contenant plusieurs unites."""

    def __init__(self, name, title, units=None):
        super().__init__(name, title)
        self._units = list(units) if units else []

    def add_unit(self, unit):
        """Ajoute une unite au semestre."""
        if not isinstance(unit, AcademicElement):
            raise TypeError("L'element doit etre academique.")
        self._units.append(unit)

    def calculate_average(self):
        """Calcule la moyenne du semestre selon les coefficients."""
        if not self._units:
            return 0

        total_coef = sum(
            sum(module.coef for module in unit._modules)
            for unit in self._units
        )

        if total_coef == 0:
            return 0

        weighted_sum = sum(
            module.calculate_average() * module.coef
            for unit in self._units
            for module in unit._modules
        )

        return weighted_sum / total_coef

    def calculate_credits(self):
        """Additionne les credits obtenus dans les unites."""
        return sum(unit.calculate_credits() for unit in self._units)
