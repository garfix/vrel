from dataclasses import dataclass
from vrel.core.functions.terms import get_variables
from vrel.entity.Atom import Atom


@dataclass(frozen=True)
class InductionRule:
    antecedent: list[Atom]
    consequent: list[Atom]

    def __str__(self) -> str:
        if len(self.antecedent) == 0:
            return str(self.antecedent) + "."
        else:
            return (
                str(self.antecedent)
                + " => "
                + ", ".join([(str(atom)) for atom in self.consequent])
                + "."
            )

    def get_all_variables(self) -> list[str]:
        variables = []
        variables.extend(get_variables(self.antecedent))
        variables.extend(get_variables(self.consequent))

        return variables
