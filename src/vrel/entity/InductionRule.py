from dataclasses import dataclass
from vrel.core.functions.terms import get_variables
from vrel.entity.Atom import Atom


@dataclass(frozen=True)
class InductionRule:
    antecedent: list[Atom]
    consequent: list[Atom]
    plan: None | list[Atom]

    def __str__(self) -> str:
        s = str(self.antecedent)

        if len(self.consequent) == 0:
            s += "."
        else:
            if self.plan:
                s += " => " + str(self.plan)
            s += " => " + ", ".join([(str(atom)) for atom in self.consequent]) + "."

        return s

    def get_all_variables(self) -> list[str]:
        variables = []
        variables.extend(get_variables(self.antecedent))
        variables.extend(get_variables(self.consequent))

        return variables
