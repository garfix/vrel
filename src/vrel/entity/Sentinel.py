from dataclasses import dataclass


@dataclass(frozen=True)
class Sentinel:

    name: str

    def __repr__(self) -> str:
        return f"S({self.name})"

    def __eq__(self, value):
        return isinstance(value, Sentinel) and self.name == value.name
