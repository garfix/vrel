from dataclasses import dataclass

from vrel.core.functions.terms import format_term
from vrel.entity.Variable import Variable


class Atom:
    name: str
    variable: Variable
    arguments: dict

    def __init__(self, variable: Variable, name: str, *args):
        self.variable = variable
        self.name = name
        self.arguments = {}

        if not isinstance(variable, Variable):
            raise Exception(f"Arg 1 must be a variable: {variable}")

        if not isinstance(name, str):
            raise Exception(f"Arg 2 must be a string: {name}")

        for index, arg in enumerate(args):
            if isinstance(arg, dict):
                self.arguments |= arg
            elif isinstance(arg, Atom) or isinstance(arg, float) or isinstance(arg, int) or isinstance(arg, str):
                key = f"ARG{index}"
                self.arguments[key] = arg
            else:
                raise Exception(f"Unknown argument type: {arg}")

    def __str__(self) -> str:
        return format_term(self, "")
