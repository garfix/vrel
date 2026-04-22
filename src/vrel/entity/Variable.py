from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:

    name: str

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, value):
        return isinstance(value, Variable) and self.name == value.name
