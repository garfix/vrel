from dataclasses import dataclass
from vrel.core.functions.terms import get_variables
from vrel.entity.Atom import Atom


@dataclass(frozen=True)
class InferenceRule:
    head: Atom
    body: list[Atom]

    def __str__(self) -> str:
        if len(self.body) == 0:
            return str(self.head) + "."
        else:
            return str(self.head) + " :- " + ", ".join([(str(atom)) for atom in self.body]) + "."

    def get_all_variables(self) -> list[str]:
        variables = []
        variables.extend(get_variables(self.head))
        variables.extend(get_variables(self.body))

        return variables
