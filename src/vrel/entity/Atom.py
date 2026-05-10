from __future__ import annotations
from dataclasses import dataclass
from vrel.entity.Sentinel import Sentinel
from vrel.entity.Variable import Variable

MODIFIER_POSITION_PRE = "modifier pre"
MODIFIER_POSITION_POST = "modifier post"
MODIFIER_POSITION_ANYWHERE = "modifier"


@dataclass(frozen=True)
class Modifier:
    atom: Atom
    variable: Variable
    position: str


class Atom:
    predicate: str
    arguments: list
    modifiers: list[Modifier]
    determiner: Atom | None
    exec: list[Atom]

    def __init__(self, *args):
        self.arguments = []
        self.modifiers = []
        self.determiner = None
        self.exec = []

        if len(args) < 1:
            raise Exception("Atom must have at least a predicate")

        if isinstance(args[0], str):
            self.predicate = args[0]
        else:
            raise Exception(f"Arg 1 must hold the predicate: {args}")

        for arg in args[1:]:
            if (
                isinstance(arg, Atom)
                or isinstance(arg, float)
                or isinstance(arg, int)
                or isinstance(arg, str)
                or isinstance(arg, Variable)
                or isinstance(arg, list)
                or isinstance(arg, Sentinel)
            ):
                self.arguments.append(arg)
            else:
                raise Exception(f"Unknown argument type: {arg}")

    def copy(self):
        a = Atom(
            self.predicate,
            *self.arguments,
        )
        a.determiner = self.determiner
        a.modifiers = [*self.modifiers]
        a.exec = [*self.exec]
        return a

    def apply_to_each_atom(self, func):
        a = self.copy()
        a.arguments = [func(arg) for arg in a.arguments]
        a.modifiers = []
        for mod in self.modifiers:
            a.modifiers.append(Modifier(variable=func(mod.variable), atom=func(mod.atom), position=mod.position))

        a.exec = [func(command) for command in a.exec]
        return a

    def flatten(self):
        a = Atom(self.predicate)
        a.arguments = self.arguments
        return a

    def with_execute(self, atoms: list[Atom]):
        a = self.copy()
        a.exec = atoms
        return a

    def with_determiner(self, determiner: Atom):
        a = self.copy()
        a.determiner = determiner
        return a

    def mod(self, atom: Atom, variable: Variable = None, position: str = MODIFIER_POSITION_ANYWHERE):
        if variable is None:
            variable_count = 0

            # for arg in atom.arguments:
            #     if isinstance(arg, Variable):
            #         for arg2 in self.arguments:
            #             if isinstance(arg2, Variable):
            #                 if arg == arg2:
            #                     variable_count += 1
            #                     variable = arg

            # for arg in atom.arguments:
            #     if isinstance(arg, Variable):
            #         variable_count += 1
            #         variable = arg
            # if variable_count != 1:
            #     print(atom.arguments)
            #     print(self.arguments)
            #     raise Exception(f"Please specify the variable for this mod: {atom}")

            # if len(atom.arguments) > 0 and isinstance(atom.arguments[0], Variable):
            # variable = atom.arguments[0]
        # elif not isinstance(variable, Variable):
        #     raise Exception(f"Is not a variable: {variable}")
        if not isinstance(atom, Atom):
            raise Exception(f"Is not an atom: {atom}")

        a = self.copy()
        a.modifiers.append(Modifier(atom, variable, position))
        a.type = type
        return a

    def get_determiner_np(self, variable: Variable):
        for mod in self.modifiers:
            if mod.atom.determiner is not None:
                for arg in mod.atom.arguments:
                    if arg == variable:
                        return mod.atom
        return None

    def get_modifier_atoms(self):
        return list(map(lambda mod: mod.atom, self.modifiers))

    def __eq__(self, value):
        return (
            isinstance(value, Atom)
            and self.predicate == value.predicate
            and self.arguments == value.arguments
            and self.modifiers == value.modifiers
            and self.determiner == value.determiner
            and self.exec == value.exec
        )

    def __repr__(self):
        from vrel.core.functions.terms import format_term

        return format_term(self)
