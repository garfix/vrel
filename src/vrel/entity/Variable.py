from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:

    name: str

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, value):
        return self.name == value.name
